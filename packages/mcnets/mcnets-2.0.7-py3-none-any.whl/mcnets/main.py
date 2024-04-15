# MCNet Dependancies
from mcnets.activations import *
from mcnets.tools import *

# Early Fitting - Ignore polynomial rank warnings
import warnings
warnings.simplefilter('ignore', np.RankWarning)


## =================== Models ==================== ##
# Primary Monte-Carlo Neural Network Model
class NeuralNetwork:
    def __init__(self, hidden_counts:'tuple[int]'=(100), activations:'tuple[str, function]'=('relu'), input_acti='identity', 
                 output_acti='identity', max_iter=1000, learning_rate_init=1, learning_rate_mode=('adaptive', 'dynamic', 'constant'), 
                 gamma=0.0025, n_iter_no_change=25, l2_reg=0, l1_reg=0, dropout=0.0, validation_fraction:float=0, early_stopping=True, 
                 quad_tol:float=-0.01, tri_tol:float=-0.01, normalize_input=False, verbose=False):
        """
        Neural Network that uses Monte-Carlo training. Can be either a regressor or classifier depending on the
        output_activation used (i.e. use sigmoid/sig for a classifier).

        - `hidden_counts`
            - List of count of units to have per hidden layer
            - Length of this list == number of hidden layers
            - Can pass an empty list to generate a model with no hidden layers
        
        - `activations`
            - List of activations (strings and/or functions) for the hidden layers with the same length as hidden_counts
            - Strings:
                - Should be one of the accepted strings below (NOT case sensitive):
                    - `'LIN'/'LINEAR'/'IDENTITY', 'RELU', 'LRELU', 'SILU', 'SIG', 'DSILU', 'TANH', 'ELU', 'ROOT', 'SQR', 'RND'`
            - Functions:
                - Should take an array, and output an array of the same size
                - Example: A ReLU function could be: `lambda x: np.maximum(x, 0)`

        - `input_acti`
            - The activation used in the input layer (before any matrix calculations). Same requirements as `activations`
        
        - `output_acti`
            - The activation used in the output layer (after all matrix calculations). Same requirements as `activations`

        - `max_iter`
            - The maxmimum iterations to use when fitting the model

        - `learning_rate_init`
            - The initial learning rate magnitude to used when fitting the model

        - `learning_rate_mode`
            - 'adaptive': Keeps learning rate constant until no improvment for `n_iter_no_change` # of iterations, then halves the learning rate
            - 'dynamic': Continually decreases the learning rate via exponential decay, with gamma as the decay factor (`rate * 2**(-iter*gamma)`)
            - 'constant': Doesn't change the learning rate throughout the fitting process

        - `gamma`
            - Exponential decay factor when using 'dynamic' learning rate mode

        - `n_iter_no_change`
            - Amount of iterations waited when using the 'adaptive' learning mode before halving the learning rate

        - `l2_reg`
            - Magnitude of the L2 regularization penalty applied

        - `l1_reg`
            - Magnitude of the L1 regularization penalty applied

        - `dropout`
            - Average (decimal) percentage of weights that aren't altered with every change

        - `validation_fraction`
            - Decimal percent of fit data put aside to use as a validation set
            - If above 0, the early stopping tolerances `quad_tol` and `tri_tol` use the validation
            score history over the training score history

        - `early_stopping`
            - Determines if the `quad_tol` and `tri_tol` early stopping methods are used

        - `quad_tol`
            - Early stopping method
            - Fits a polynomial (degree 2) to the current training scores during fitting
            - If the polynomial has a tangent/slope value less than this tolerance, training stops
            - If None:
                - Doesn't consider this for early stopping, even if early_stopping is True
                - Helpful for only considering one of the tols (quad or tri)

        - `tri_tol`
            - Early stopping method
            - Fits a polynomial (degree 3) to the current training scores during fitting
            - If the polynomial has a tangent/slope value less than this tolerance, training stops
            - If None:
                - Doesn't consider this for early stopping, even if early_stopping is True
                - Helpful for only considering one of the tols (quad or tri)

        - `normalize_input`
            - Automatically normalize input data
        """

        # Assemble hidden counts to a list
        if isinstance(hidden_counts, list):
            self.hidden_counts = hidden_counts
        elif isinstance(hidden_counts, tuple):
            self.hidden_counts = list(hidden_counts)
        elif isinstance(hidden_counts, (int)):
            self.hidden_counts = [hidden_counts]
        else:
            raise ValueError("Unknown type given for hidden_counts")

        # Assemble activations to a list
        if isinstance(activations, list):
            self.activations = activations
        elif isinstance(activations, tuple):
            self.activations = list(activations)
        elif isinstance(activations, str) or callable(activations):
            self.activations = [activations]*len(self.hidden_counts)
        else:
            raise ValueError("Unknown type given for activations")

        # Main params
        self.input_acti = input_acti
        self.output_acti = output_acti
        self.max_iter = max_iter
        self.learning_rate_init = learning_rate_init
        self.learning_rate_mode = 'adaptive' if isinstance(learning_rate_mode, tuple) else learning_rate_mode
        self.gamma = gamma
        self.n_iter_no_change = n_iter_no_change
        self.l2_reg = l2_reg
        self.l1_reg = l1_reg
        self.dropout = dropout
        self.val_frac = validation_fraction
        self.stop_early = early_stopping
        self.quad_tol = quad_tol
        self.tri_tol = tri_tol
        self.normalize_input = normalize_input
        self.verbose = verbose

        # Fit-generated params
        self._use_score_history = 'train' if self.val_frac <= 0 else 'val'
        self._has_normalized_info = False
        self._normalized_mean = None
        self._normalized_stdev = None
        self._is_fitted = False
        self.input_size = None
        self.output_size = None
        self.weights = []
        self.biases = []

        # Initial checks
        if len(self.hidden_counts) != len(self.activations):
            raise ValueError(f"Length of hidden_counts ({self.hidden_counts}) != Length of activations ({self.activations})")
        
        # Compile activations
        for i, af in enumerate(self.activations):
            if type(af) == str:
                try:
                    self.activations[i] = AFDict[af.upper()]
                except:
                    raise ValueError(f"Activation name '{af}' is not in the accepted activations")
        
        if type(self.input_acti) == str:
            try:
                self.input_acti = AFDict[self.input_acti.upper()]
            except:
                if not callable(input_acti):
                    raise ValueError(f"Input activation name '{self.input_acti}' is not in the accepted activations")
                else:
                    self.input_acti = input_acti
            
        if type(self.output_acti) == str:
            try:
                self.output_acti = AFDict[self.output_acti.upper()]
            except:
                if not callable(self.output_acti):
                    raise ValueError(f"Output activation name '{self.output_acti}' is not in the accepted activations")
                else:
                    self.output_acti = self.output_acti

    def set_weights(self, new_weights:'list[np.ndarray]'):
        self.weights = [wi.copy() for wi in new_weights]

    def set_biases(self, new_biases:'list[np.ndarray]'):
        self.biases = [bi.copy() for bi in new_biases]

    def get_weights(self):
        return [wi.copy() for wi in self.weights]
    
    def get_biases(self):
        return [bi.copy() for bi in self.biases]

    def predict(self, X:np.ndarray):
        # Normalize input if wequested
        if self.normalize_input and self._has_normalized_info:
            X = (X - self._normalized_mean) / self._normalized_stdev
        elif self.normalize_input and not self._has_normalized_info:
            raise ValueError("Model should have Mean and StDev info for input data normalization but it doesnt!")

        # Apply initial activation
        X = self.input_acti(X)

        # Hidden Layers yipeeeeeeeeeee
        for afunc, W, B in zip(self.activations+[self.output_acti], self.weights, self.biases):
            X = afunc(np.dot(X, W) + B)

        # Shape accordingly
        if self.output_size == 1:
            X = X.flatten()
        return X
    
    def predict_layer(self, X:np.ndarray, from_h_layer:int):
        """Specialized predict function to allow for getting model features from
        any of the hidden layers (specified from `layer`)
        
        - `from_h_layer`:
            - Integer deciding which hidden layer to snatch features from
            - Should be a value in the domain [1, (# of hidden layers)]
        """
        # Prevent fetching outputs of layers that dont exist =)
        if from_h_layer > len(self.hidden_counts):
            raise ValueError(f"Features from hidden layer #{from_h_layer} requested but the model only has {len(self.hidden_counts)} hidden layers!")
        from_h_layer = np.clip(from_h_layer, 1, len(self.hidden_counts))
        
        ## Modified prediction algorithm ##
        # Normalize input if wequested
        if self.normalize_input and self._has_normalized_info:
            X = (X - self._normalized_mean) / self._normalized_stdev
        elif self.normalize_input and not self._has_normalized_info:
            raise ValueError("Model should have Mean and StDev info for input data normalization but it doesnt!")

        # Apply initial activation
        X = self.input_acti(X)

        # Hidden Layers yipeeeeeeeeeee
        for afunc, W, B in zip(list(self.activations+[self.output_acti])[:from_h_layer], self.weights[:from_h_layer], self.biases[:from_h_layer]):
            X = afunc(np.dot(X, W) + B)

        # Shape accordingly
        return X.flatten() if self.output_acti == 1 else X
        
    def _current_l2_penalty(self):
        return self.l2_reg*np.sum([np.sum(wi**2) for wi in self.get_weights()])
    
    def _current_l1_penalty(self):
        return self.l1_reg*np.sum([np.sum(np.abs(wi)) for wi in self.get_weights()])
    
    def score(self, X, Y, score_type='r2'):
        return score_model(self, X, Y, method=score_type) - self._current_l2_penalty() - self._current_l1_penalty()
    
    def _initialize_model(self, input_size, output_size, force_generate=False):
        """Generates the models weights and biases with the given input and ouput size.
        Can be forced to regen (if already previously fitted) by setting force_generate to True."""
        if not self._is_fitted or force_generate:
            # Get feature sizes
            self.input_size = input_size
            self.output_size = output_size

            # Make Weights
            self.weights = [2*np.random.rand(s1, s2)-1 for s1, s2 in zip([self.input_size]+self.hidden_counts, self.hidden_counts+[self.output_size])]
            self.biases  = [2*np.random.rand(s1)-1 for s1 in self.hidden_counts+[self.output_size]]

            # Complete
            self._is_fitted = True
    
    def fit(self, X:np.ndarray, Y:np.ndarray, score_type='r2'):
        """Fit the model to the given data. 
        
        Returns a dict with the training score/error history under 'train' and the validation history under 'val'.
        """

        # History dict
        history = {'train': [], 'val': []}

        # Train/Validation split
        if self.val_frac > 0:
            xt, xv, yt, yv = TTSplit(X, Y, percent_train=(1-self.val_frac))
        else:
            xv = None; yv = None
            xt = X.copy()
            yt = Y.copy()

        # Make val score function for easy handling of both cases (val_frac == 0 and val_frac > 0)
        def val_score(self:NeuralNetwork, xv, yv, score_type=score_type):
            if self.val_frac <= 0:
                return 0
            else:
                return self.score(xv, yv, score_type=score_type)
            
        # Get normalization info if applicable
        if not self._is_fitted and self.normalize_input:
            msinfo = normalize(X)[1]
            self._normalized_mean = msinfo[0]
            self._normalized_stdev = msinfo[1]
            self._has_normalized_info = True

        # Generate model
        self._initialize_model(input_size=1 if len(X.shape)==1 else X.shape[1],
                               output_size=1 if len(Y.shape)==1 else Y.shape[1],
                               force_generate=False)

        # Single Column inputs - check for correct size (len(X), 1)
        if len(X.shape) == 1:
            print(f"MCNet WARN: X seems to be 1 column, but has shape {X.shape} not {(len(X), 1)} (this will be corrected but reshape X to avoid this warning).")
            X = X.reshape((len(X), 1))

        # Initial stats
        score = self.score(X, Y, score_type=score_type) if self.val_frac <= 0 else self.score(xt, yt, score_type=score_type)
        current_rate = self.learning_rate_init
        i_last_improved = 0

        # Update history
        history['train'].append(score)
        history['val'].append(val_score(self, xv, yv, score_type=score_type))

        # Main iteration loop
        for i in range(self.max_iter):
            # Get learning rate
            if self.learning_rate_mode == 'dynamic':
                current_rate = self.learning_rate_init * 2**(-i * self.gamma)
            elif self.learning_rate_mode == 'adaptive':
                if i-i_last_improved >= self.n_iter_no_change:
                    current_rate /= 2
                    i_last_improved = i

            # Test tweaking weights
            init_weights = self.get_weights()
            for ind in range(len(init_weights)):
                # Get dropout filter/mask with dropout
                if self.dropout > 0:
                    mask = np.random.random(self.weights[ind].shape)
                    mask[mask < self.dropout] = 0
                    mask[mask > self.dropout] = 1
                    adjustment = mask * np.random.random(self.weights[ind].shape)

                # Get adjustment with no dropout
                else:
                    adjustment = np.random.random(self.weights[ind].shape)

                # Modify weights using above adjustment (scaled to [-learning_rate, +learning_rate])
                self.weights[ind] += current_rate*(2*adjustment - 1)

                # Get models score with modified weights
                test_score = self.score(X, Y, score_type=score_type) if self.val_frac <= 0 else self.score(xt, yt, score_type=score_type)

                # Keep weights and set new best score if better
                if test_score > score:
                    score = test_score
                    i_last_improved = i

                    # Update history
                    history['train'].append(score)
                    history['val'].append(val_score(self, xv, yv, score_type=score_type))

                    # Do early stopping calculations (only after initial bit of training for better polynomials)
                    if self.stop_early and i >= 0.1*self.max_iter:
                        ## Build and check polynomial fits for early stopping conditions ##
                        poly_x = [*range(len(history[self._use_score_history]))]

                        ## Quad Tol check #
                        if self.quad_tol != None:
                            # Coefficients
                            p2_coefs = np.polyfit(poly_x, history[self._use_score_history], deg=2)

                            # Y (score) predictions
                            p2_y = np.polyval(p2_coefs, poly_x)
                            # p2_y = [sum([ci*x**(2-i) for i, ci in enumerate(p2_coefs)]) for x in poly_x]

                            # Numerical tangents
                            dp2_y = [y1-y2 for y1, y2 in zip(p2_y[1:], p2_y[:-1])]

                            # Check min quad tangent slope
                            if min(dp2_y) < self.quad_tol:
                                if self.verbose:
                                    print(f"Itr: {i+1}/{self.max_iter} | {score_type.upper()}: {score:.6f} | Learning Rate: {current_rate}")
                                    print("Training Stopped: quad tolerance has been surpassed")
                                return history
                            
                        ## Tri Tol check #
                        if self.tri_tol != None:
                            # Coefficients
                            p3_coefs = np.polyfit(poly_x, history[self._use_score_history], deg=3)

                            # Y (score) predictions
                            p3_y = np.polyval(p3_coefs, poly_x)
                            # p3_y = [sum([ci*x**(3-i) for i, ci in enumerate(p3_coefs)]) for x in poly_x]

                            # Numerical tangents
                            dp3_y = [y1-y2 for y1, y2 in zip(p3_y[1:], p3_y[:-1])]

                            # Check min quad tangent slope
                            if min(dp3_y) < self.tri_tol:
                                if self.verbose:
                                    print(f"Itr: {i+1}/{self.max_iter} | {score_type.upper()}: {score:.6f} | Learning Rate: {current_rate}")
                                    print("Training Stopped: tri tolerance has been surpassed")
                                return history

                # Reset weights to original values if not better
                else:
                    self.weights[ind] = init_weights[ind].copy()

            # Status
            if self.verbose:
                print(f"Itr: {i+1}/{self.max_iter} | {score_type.upper()}: {score:.6f} | Learning Rate: {current_rate}      ", end='\r')

        # Final printout
        if self.verbose:
            print(f"Itr: {i+1}/{self.max_iter} | {score_type.upper()}: {score:.6f} | Learning Rate: {current_rate}")
        return history

    def save(self, name:str):
        save_model(self, name=name)

    def get_param_ranges_for_optuna(self):
        """Returns a dictionary of params and their possible values either via tuples of (min_val, max_val)
        or lists for discrete categorical params/options.
        
        Params not included in the dictionary:
        - `hidden_counts`
        - `activations`
        - `verbose`
        
        These params should be directly set as desired in an optimizer."""

        return {
            'input_acti': ['LIN', 'RELU', 'LRELU', 'SILU', 'SIG', 'DSILU', 'TANH', 'ELU', 'ROOT', 'SQR', 'RND'],
            'output_acti': ['LIN', 'RELU', 'LRELU', 'SILU', 'SIG', 'DSILU', 'TANH', 'ELU', 'ROOT', 'SQR', 'RND'],
            'max_iter': (1, 10000),
            'learning_rate_init': (1e-3, 5),
            'learning_rate_mode': ['adaptive', 'dynamic', 'constant'],
            'gamma': (1e-6, 10),
            'n_iter_no_change': (1, 5000),
            'l2_reg': (1e-10, 1),
            'l1_reg': (1e-10, 1),
            'dropout': (0, 0.9), 
            'validation_fraction': (0.1, 0.75),
            'early_stopping': [True, False],
            'quad_tol': (-1, 1),
            'tri_tol': (-1, 1),
            'normalize_input': [True, False],
        }

    def copy(self):
        """Returns a deep copy of the model"""
        return copy.deepcopy(self)
    
    def make_mutation(self, learning_rate=1):
        """Returns a copy of the model with weights randomly via values
        in the range [-learning_rate, +learning_rate]."""
        # Get a model copy, adjust its weights
        new = self.copy()
        for wi in new.weights:
            wi += learning_rate*(2*np.random.random(wi.shape)-1)
        return new

# Large flexible "polynomial" 
class SoupRegressor:
    def __init__(self, use_tan=False, round_threshold=1e-5, max_iter=100, dropout=0., learning_rate_init=20., 
                 learning_rate_mode:str=('dynamic', 'adaptive', 'constant'), gamma=50, n_iter_no_change=10, 
                 use_biases=True, trainable_biases=False, l1_reg=0., l2_reg=0., verbose=False):
        """
        Creates and combines outputs of large ""polynomials"" made for every X feature given in .fit(). Only
        fits to one target.

        - `use_tan`
            - Three TAN(x) terms are included in f(x), but due to the asymptotic nature of TAN, they
              can actually hurt model preformance. So, this is disabled by default, but left as a
              setting to try anyways.

        - `round_threshold`
            - When adjusting the coefficients of the model, if a single coefficient's magnitude falls
              below this threshold, it is rounded to 0. This makes it easier for the model to completely
              remove terms from its various f(x) equations if it finds that is better.

        - `max_iter`
            - Maximum iterations used to train the model
            - As of V2.0.3 there is no early stopping for this model, so this is simply the number of 
            training iterations completed

        - `dropout`
            - Average (decimal) percent of coefficients ignored (not trained) per sub iteration

        - `learning_rate_init`
            - Initial learning rate
            - Note that this model type typically requires a much higher learning rate than others so
            the typical value of 1 is too slow more often than not

        - `learning_rate_mode`
            - 'adaptive': Keeps learning rate constant until no improvment for `n_iter_no_change` # of iterations, then halves the learning rate
            - 'dynamic': Continually decreases the learning rate via exponential decay, with gamma as the decay factor (`rate * 2**(-iter*gamma)`)
            - 'constant': Doesn't change the learning rate throughout the fitting process

        - `gamma`
            - Exponential decay factor when using 'dynamic' learning rate mode

        - `n_iter_no_change`
            - Amount of iterations waited when using the 'adaptive' learning mode before halving the learning rate

        - `use_biases`
            - Decides if a constant [-1, 1] is included at the end of each feature's f(x)

        - `trainable_biases`
            - Decides of the above constants are trainable

        - `l2_reg`
            - Magnitude of the L2 regularization penalty applied

        - `l1_reg`
            - Magnitude of the L1 regularization penalty applied

        ## Technical Breakdown

        For each column of data, generates a function of best fit of the form:

        f_i(x) = k0 + k1*(|x|**0.5) + k2*(x) + k3*(x**2) + k4*sin(x/3) + k5*sin(x) + k6*sin(3x) + 

               k7*cos(x/3) + k8*cos(x) + k9*cos(3x) + k10*tan(x/3) + k11*tan(x) + k12*tan(3x) + 

               k13*e**(x/3) + k14*e**(x) + k15*e**(3x) + k16*e**(-x/3) + k17*e**(-x) + k18*e**(-3x)

        There is an f(x) for every x feature. This means for N features the net model is:

        F(x) = SUM[f_i(x)] for i=[0, 1, ..., N-1]
        """

        # Unchanging attributes
        self.FUNCTION_LENGTH = 19 if not use_biases else 20
        self.USE_TAN = use_tan
        self.ROUND = round_threshold

        # Fit params
        self.ieta = max_iter
        self.dropout = dropout
        self.init_rate = learning_rate_init
        self.learning_mode = 'adaptive' if isinstance(learning_rate_mode, tuple) else learning_rate_mode
        self.gamma = gamma
        self.n_iter_no_change = n_iter_no_change
        self.use_biases = use_biases
        self.train_biases = trainable_biases
        self.l1_reg = l1_reg
        self.l2_reg = l2_reg
        self.verbose = verbose

        # Attributes generated in fit
        self.coefs = 0
        self.num_features = 0
        self.parameters = 0
        self.fitted = False

    ## Model Functions ##
    def predict(self, X:np.ndarray, run_debug=False):
        """
        Calculates each f(x) described, for each row in X.
        """

        # Verify the shape of X (and num_features)
        if run_debug:
            given_size = 1 if len(X.shape) == 1 else X.shape[1]
            if self.num_features != given_size:
                raise ValueError(f"Expected X array shape of ({len(X)}, {self.num_features}), got {X.shape}")
            
        # Main function, per feature
        def f(x, col_index):
            # Get function coefficients for this feature
            k = self.coefs[:, col_index].flatten()

            # Complete f(x) prediction, add k[19] (bias) if included in model
            SUM = k[0] + k[1]*(np.abs(x)**0.5) + k[2]*x + k[3]*(x**2) + k[4]*np.sin(x/3) + k[5]*np.sin(x) + k[6]*np.sin(3*x) + \
                  k[7]*np.cos(x/3) + k[8]*np.cos(x) + k[9]*np.cos(3*x) + self.USE_TAN*k[10]*np.tan(x/3) + self.USE_TAN*k[11]*np.tan(x) + self.USE_TAN*k[12]*np.tan(3*x) + \
                  k[13]*np.exp(x/3) + k[14]*np.exp(x) + k[15]*np.exp(3*x) + k[16]*np.exp(-x/3) + k[17]*np.exp(-x) + k[18]*np.exp(-3*x)
            
            if self.use_biases:
                SUM += k[19]
            
            return SUM
        
        # Calculate the sum described in INIT
        result = 0
        for col_index in range(self.num_features):
            result += f(X[:, col_index], col_index=col_index)
        return result
    
    def _initialize_model(self, input_size, force_generate=False):
        if not self.fitted or force_generate:
            # Setup coefficients
            self.num_features = input_size
            self.coefs = 2*np.random.rand(self.FUNCTION_LENGTH, self.num_features) - 1
            
            # Confirm initial fit
            self.parameters = self.coefs.size
            self.fitted = True

    def fit(self, X, Y, score_type='r2'):
        # Check if model initial fit complete
        self._initialize_model(input_size=1 if len(X.shape)==1 else X.shape[1], force_generate=False)

        # Get coefs to adjust (include or exclude bias, the last one)
        if self.use_biases and not self.train_biases:
            end_len = self.FUNCTION_LENGTH - 1
        else:
            end_len = self.FUNCTION_LENGTH

        # Tweak params for N iterations
        i_last_improved = 0
        current_rate = self.init_rate
        score = self.score(X, Y, method=score_type)
        for itr in range(self.ieta):
            # Get dropout filter and apply it (discards changing drapout % num of coefficients)
            filt = np.random.rand(end_len) > self.dropout

            # Get learning rate
            if self.learning_mode == 'dynamic':
                current_rate = self.learning_rate_init * 2**(-itr * self.gamma)
            elif self.learning_mode == 'adaptive':
                if itr-i_last_improved >= self.n_iter_no_change:
                    current_rate /= 2
                    i_last_improved = itr

            # Loop over each f(x) coefs (self.coefs cols per feature)
            for c in range(self.coefs.shape[1]):
                # Get original values to reset to if no improvement
                init_coefs = self.coefs[:end_len, c].copy()

                # Make adjustment
                self.coefs[:end_len, c] += current_rate*(2*filt*np.random.rand(end_len) - 1)

                # Test adjustment
                new_score = self.score(X, Y, method=score_type)
                if new_score > score:
                    # Keep new coefs, set new best score
                    score = new_score
                    i_last_improved = itr

                    # Round coefs below threshold to 0
                    self.coefs[np.abs(self.coefs) < self.ROUND] = 0
                else:
                    # Worse score, reset coefs changed
                    self.coefs[:end_len, c] = init_coefs

            # Print status
            if self.verbose:
                print(f"Itr. #{itr+1} | Score = {format(score, '.6f')} | Learning Rate = {current_rate:.6f}        ", end='\r')
        
        if self.verbose:
            print(f"Itr. #{itr+1} | Score = {format(score, '.6f')} | Learning Rate = {current_rate:.6f}        ")

    def _current_l2_penalty(self):
        return self.l2_reg*np.sum(self.coefs**2)
    
    def _current_l1_penalty(self):
        return self.l1_reg*np.sum(np.abs(self.coefs))

    def score(self, X, Y, method='r2'):
        return score_model(self, X, Y, method=method) - self._current_l2_penalty() - self._current_l1_penalty()
    
    def copy(self):
        """Returns a copy of the model"""
        return copy.deepcopy(self)


## ================== Ensembles ================== ##
# Standard Ensemble #
class StandardEnsemble():
    def __init__(self, models:list) -> None:
        """
        A wrapper for combining multiple models into one. By default, uses weights
        equal weights for each individual model given unless `optimize_model_weights`
        is called.

        - `models`
            - The list of models to make an ensemble out of
        """
        self.models = models
        self.model_weights = [1/len(self.models) for _ in range(len(self.models))]

    def fit(self, X, Y, score_type='r2'):
        """Fit all of the individual models in the ensemble"""
        # Fit all the models
        for mi in self.models:
            try:
                mi.fit(X, Y, score_type=score_type)
            except TypeError as e:
                if 'unexpected keyword argument' in str(e):
                    mi.fit(X, Y)
                else:
                    raise ValueError(e)

    def predict(self, X):
        # Combine all model outputs
        output = 0
        for mi, wi in zip(self.models, self.model_weights):
            output += wi*mi.predict(X)
        return output

    def optimize_model_weights(self, X, Y, verbose=False):
        """Tests each individual model by scoring them via a 5-fold cross validation
        to the given data. All of these scores are normalized, and then used as the
        individual models' effective weight in the ensemble."""
        scores = [cross_val(mi, X, Y, score_type='r2', verbose=verbose).mean() for mi in self.models]
        scores = [s/sum(scores) for s in scores]
        self.model_weights = scores

    def score(self, X, Y, score_type='r2'):
        return score_model(self, X, Y, method=score_type)


# Dictator Ensemble #
class DictatorEnsemble():
    def __init__(self, base_models:list, dictator_model) -> None:
        """
        Adds a main (dictator) model to a standard ensemble made
        from the base models. The main model gets the X and outputs
        from the base models as an input to create the final output.
        """
        self.ensemble = StandardEnsemble(models=base_models)
        self.dictator = dictator_model

    def _base_predict(self, X):
        # Gather all the normies outputs for the dictator to use
        for i, mi in enumerate(self.ensemble.models):
            if i == 0:
                # Get first prediction; set to column type for stacking purposes
                # (This will be the dictator's 'X')
                output = mi.predict(X)
                if output.ndim == 1:
                    output = output.reshape((output.size, 1))
            else:
                # Get othe predictions, set to column type
                new_out = mi.predict(X)
                if new_out.ndim == 1:
                    new_out = new_out.reshape((new_out.size, 1))
                output = np.hstack([output, new_out])
        return output
    
    def predict(self, X):
        # Use base model predictions to get actual predictions from dictator
        options = self._base_predict(X)
        return self.dictator.predict(options)

    def fit(self, X, Y, score_type='r2'):
        # Standard fitting
        self.ensemble.fit(X, Y, score_type=score_type)

        # Fit dictator
        options = self._base_predict(X) 
        try:
            self.dictator.fit(options, Y, score_type=score_type)
        except TypeError as e:
            if 'got an unexpected keyword argument' in str(e):
                self.dictator.fit(options, Y)
            else:
                raise ValueError(e)
        

    def score(self, X, Y, score_type='r2'):
        return score_model(self, X, Y, method=score_type)
    

## ================== High-Level Tools ================== ##
def test_activations(X:np.ndarray, Y:np.ndarray, custom_activations=(), only_custom=False,
                     cv=5, cv_score_type='r2', nn_kwargs:dict={}, verbose=True):
    """Builds and test 1-hidden layer Neural Networks each with
    a different activation to test how well they fit to the given data.

    Returns a sorted (greatest to least) list of (scores, function)

    - `custom_activations`
        - List of other (external) activation functions to test to the data
    - `only_custom`
        - Decides if only the custom activations are tested (as to not waste
        time testing the normal ones).
    - `cv`
        - Number of folds to use for the cross validation test, per activation
    - `nn_args`
        - Arguments to pass to the `NeuralNetwork` test models made
    - `verbose`
        - Report which CV is currently being done & display score results at end
    """
    # Setup base arguments in args (if not already sepcified)
    if "activations" in nn_kwargs.keys():
        nn_kwargs.pop("activations")
    if "hidden_counts" not in nn_kwargs.keys():
        nn_kwargs["hidden_counts"] = (25)

    # Get activations to test
    af_test_funcs = list(custom_activations)
    af_test_names = [f.__name__ if callable(f) else f for f in af_test_funcs]

    if not only_custom:
        af_test_funcs += list(AFDict.values())[2:-3]  # ignore extra lin/linear & experimental last 3
        af_test_names += list(AFDict.keys())[2:-3]    # ignore extra lin/linear & experimental last 3

    # Test all activations
    scores = []
    for i, af in enumerate(af_test_funcs):
        # Make test model
        mod = NeuralNetwork(activations=(af), **nn_kwargs)
        
        # Test it and record average score
        scores.append(cross_val(mod, X, Y, score_type=cv_score_type, cv=cv, verbose=False).mean())
        if verbose:
            print(f'Finished CV #{i+1}/{len(af_test_funcs)}', end='\r')

    # Report best activations and their names
    if verbose:
        # Sort results (Greatest to Smallest)
        scores_names = list(zip(scores, af_test_names))
        scores_names.sort(reverse=True)

        # Report scores and such and yeah
        s1 = 'Activation Tested'
        s2 = 'Avg. Cross Val Score'
        print('|', s1, '|', s2, '|')
        print('='*(len(s1+s2) + 7))
        for s, afi in scores_names:
            s1 = f'{afi}'.center(len(s1))
            s2 = f'{s:.6f}'.center(len(s2))
            print('|', s1, '|', s2, '|')

    # Return a sorted zip of (scores, functions)
    scores_funcs = list(zip(scores, af_test_funcs))
    scores_funcs.sort(reverse=True)
    return scores_funcs


## Libraries ##
AFDict = {
        "LIN": lin,
        "LINEAR": lin,
        "IDENTITY": lin,
        "RELU": relu,
        "LRELU": lrelu,
        "SILU": silu,
        "SIG": sig,
        "DSILU": dsilu,
        "TANH": tanh,
        "ELU": elu,
        "ROOT": root,
        "SQR": sqr,
        "RND": rnd,
        "RESU": resu,
        "RESU2": resu2,
        "EXP": exp
    }


## Neat Paper/Other References ##
"""
1. SILU and dSILU activation functions
Stefan Elfwing, Eiji Uchibe, Kenji Doya,
Sigmoid-weighted linear units for neural network function approximation in reinforcement learning,
Neural Networks,
Volume 107,
2018,
Pages 3-11,
ISSN 0893-6080,
https://doi.org/10.1016/j.neunet.2017.12.012.
(https://www.sciencedirect.com/science/article/pii/S0893608017302976)
"""