# Imports
from joblib import dump, load
from random import sample
import numpy as np
import copy

## Main Tools ##
def save_model(model, name:str):
    """
    Load the model object saved under the given name
    """
    dump(model, filename=name)

def load_model(name:str):
    """
    Uses joblib function 'load' to recall a model object previous saved
    """
    try:
        return load(name)
    except:
        raise ValueError("Could not find a model with the given name")

def TTSplit(X:np.ndarray, Y:np.ndarray, percent_train:float = 0.7):
    """
    Universal Train-Test data split via random selection.

    Returns in the order `x_train, x_test, y_train, y_test`
    
    - `percent_train`
        - Sets the amount of data given back for training data, 
          while the rest is sent into the testing data set
    """

    # Scale percent
    if percent_train < 1:
        percent_train *= 100

    # Defaults
    xTest = []
    yTest = []
    xTrain = []
    yTrain = []

    # Generate the indicies used for collecting train data
    data_length = X.shape[0]
    num_train = round(data_length * percent_train/100)
    num_test = data_length - num_train
    trainIndicies = sample(range(data_length), num_train)
    trainIndicies.sort()

    # All-in-one train/test collector (sorted method)
    crntIndex = 0
    while crntIndex < data_length:
        # Check if its a training index
        if len(trainIndicies) >= 1:
            if crntIndex == trainIndicies[0]:
                xTrain.append(X[crntIndex])
                yTrain.append(Y[crntIndex])
                
                trainIndicies.pop(0)
                crntIndex += 1
            # Else add to test data
            else:
                xTest.append(X[crntIndex])
                yTest.append(Y[crntIndex])

                crntIndex += 1

        # Else add to test data
        else:
            xTest.append(X[crntIndex])
            yTest.append(Y[crntIndex])

            crntIndex += 1

    # Shape data lists (accounting for 1D lists)
    xTrain = np.array(xTrain).reshape((num_train) if X.ndim == 1 else (num_train, X.shape[1]))
    xTest = np.array(xTest).reshape((num_test) if X.ndim == 1 else (num_test, X.shape[1]))

    yTrain = np.array(yTrain).reshape((num_train) if Y.ndim == 1 else (num_train, Y.shape[1]))
    yTest = np.array(yTest).reshape((num_test) if Y.ndim == 1 else (num_test, Y.shape[1]))

    return xTrain, xTest, yTrain, yTest

def cross_val(model, X, Y, cv=5, score_type=('r2'), return_models=False, verbose=False, **kwargs) -> np.ndarray:
    """
    Cross validation of model using X and Y with N number of splits

    ## Params

    - `cv`
        - Number of train/validation split tests to complete

    - `scoreType`
        - One of the score/error functions avalible in score()
        - ['r2', 'sse', 'mae', 'mse', 'rae', 'acc']
        - If a function is given, should be the form:
            - scorer_func(predictor, X, Y)

    - `return_models`
        - If True, returns (models, weights) from the models tested and their
          weights derived from their score normalized to all other's scores.

    - `verbose`
        - 0 = No output printing
        - 1 = Outputs current step/progress
    """

    # Old 'N' kwarg for cv
    if 'N' in kwargs.keys():
        cv = kwargs['N']

    if 'scoreType' in kwargs.keys():
        score_type = kwargs['scoreType']

    # Check for enough data 
    if len(X) < cv:
        raise ValueError(f"Not enough data for {cv} cycles")

    # Verbose settings
    step_verbose = verbose 

    # Main loop
    if return_models:
        models = []

    base_model = copy.deepcopy(model)

    scores = []
    step = round(len(X) / cv)
    for n in range(cv):
        # Data Split
        start = n*step
        if n == cv-1:
            stop = len(X)
        else:
            stop  = (n+1)*step

        X_val = X[start:stop+1]
        Y_val = Y[start:stop+1]

        if len(X.shape) > 1:
            X_train = np.row_stack([X[:start], X[stop+1:]])
        else:
            X_train = np.array(X[:start].tolist() + X[stop+1:].tolist())

        if len(Y.shape) > 1:
            Y_train = np.row_stack([Y[:start], Y[stop+1:]])
        else:
            Y_train = np.array(Y[:start].tolist() + Y[stop+1:].tolist())

        # Train model
        model = copy.deepcopy(base_model)
        try:
            model.fit(X_train, Y_train, score_type=score_type)
        except:
            model.fit(X_train, Y_train)

        if return_models:
            models.append(model)

        # Record model score
        try: # MC models (extra .score options)
            scores.append(model.score(X_val, Y_val, score_type=score_type))
        except: # Other lame models (no extra .score options) ((jk I luv u other models))
            scores.append(model.score(X_val, Y_val))

        # Print step results
        if step_verbose:
            print(f"Cross-Validation: Step {n+1}/{cv} Complete     ", end='\r')

    # Generate model weights if needed
    if return_models:
        weights = [m.score(X, Y) for m in models]
        weights = np.array(weights)
        weights /= np.sum(weights)
        weights = weights.tolist()

    # Finish
    if step_verbose:
        print(f"Mean Model {score_type} Validation Score/Error = {np.mean(scores):.6f} +- {np.std(scores):.6f}")

    if return_models:
        return models, weights
    else:
        return np.array(scores)

def cv_score(model, X, Y, cv=5, score_type=('r2')):
    return cross_val(model=model, X=X, Y=Y, cv=cv, score_type=score_type, verbose=False).mean()

def cv_predict(model, X, Y, cv=5, score_type=('r2')):
    models, weights = cross_val(model=model, X=X, Y=Y, cv=cv, score_type=score_type, return_models=True, verbose=False)
    
    output = 0
    for mi, wi in zip(models, weights):
        output += wi*mi.predict(X)

    return output

def score(ytrue, ypred, method='r2') -> float:
    """
    Main scorer function given a model's output and true values.

    - `method`
        - 'r2': R^2 Score
        - 'sse': -Sum Squared Error
        - 'mse': -Mean Squared Error
        - 'mre': -Root Mean Squared Error
        - 'mae': -Mean Absolute Error
        - 'rae': Custom R^2-like Score
        - 'acc'/'accuracy': Accuracy Score
        - Function: form of `scorer(ytrue, ypred)`
    """

    # Force correct case
    method = method.lower()

    ## R^2 Method ##
    if method == 'r2':
        return r2d2(ypred, ytrue)

    ## Sum Squared Error ##
    elif method == 'sse':
        return -np.sum((ypred - ytrue)**2)
    
    ## Mean Squared Error ##
    elif method == 'mse':
        return -np.sum((ypred - ytrue)**2)/ypred.size
    
    ## Mean Root Error ##
    elif method == 'mre':
        return -(np.sum((ypred - ytrue)**2) / len(ypred))**0.5

    ## Mean Absolute Error ##
    elif method == 'mae':
        return -(1/len(ypred)) * np.sum(np.abs(np.array(ypred) - ytrue))

    ## RAE Score ##
    elif method == 'rae':
        return raeScore(ytrue, ypred)
    
    ## Accuracy Score ##
    elif method in ['acc', 'accuracy']:
        return np.sum(ypred == ytrue) / ypred.size
    
    ## Custom Function ##
    elif callable(method):
        return method(ytrue, ypred)

    # Raise error if one of the possible methods was not given
    else:
        raise ValueError(f"Given score type '{method.upper()}' is not one of the avalible types.")

def score_model(model, X:np.ndarray, ytrue:np.ndarray, method='r2') -> float:
    """
    Main scorer function given a model, input data, and true values.

    - `method`
        - 'r2': R^2 Score
        - 'sse': -Sum Squared Error
        - 'mre': -Root Mean Squared Error
        - 'mae': -Mean Absolute Error
        - 'rae': Custom R^2-like Score
        - 'acc'/'accuracy': Accuracy Score
        - Function: form of `scorer(model, X, ytrue)`
    """

    # Force lowercase
    if not callable(method):
        method = method.lower()
    
    # Get model output
    ypred = model.predict(X)

    # For callable scorers given
    if callable(method):
        return method(model, X, ytrue)
    
    # Otherwise use main score function
    else:
        # Try to include L2/L1 penalties
        try:
            return score(ytrue, ypred, method=method) - model._current_l2_penalty() - model._current_l1_penalty()
        except:
            return score(ytrue, ypred, method=method)


## Small/Helpers ##
## Helper/Smol Functions ##
def r2d2(yModel:np.ndarray, yTrue:np.ndarray):
    """
    Returns the R^2 value of the model values (yModel) against the true
    y data (yTrue).
    """

    # List checking for idoits like me
    if type(yModel) == list:
        yModel = np.array(yModel)
    if type(yTrue) == list:
        yTrue = np.array(yTrue)

    # Check if needs to be flattened
    # if len(yTrue.shape) == 1 and len(yModel.shape) > 1:
    #     yModel = yModel.flatten()
    
    # if len(yTrue.shape) > 1:
    #     if yTrue.shape[1] == 1:
    #         yTrue = yTrue.flatten()
    #         yModel = yModel.flatten()
    
    yTrue = yTrue.reshape(yModel.shape)

    # R2 Calc
    yMean = np.mean(yTrue)
    RES = np.sum(np.clip(yTrue - yModel, -1e154, 1e154) ** 2)
    TOT = np.sum((yTrue - yMean) ** 2)
    if TOT == 0:
        TOT = np.inf

    return 1 - (RES / TOT)
    
def raeScore(yTrue:np.ndarray, yPred:np.ndarray):
    """
    ## Relative Average Error Score

    ### Preforms the following calculation sequence:

    #### 1 Element-wise Absolute Relative Error (ARE)

        - score_ij = |yTrue_ij - yPred_ij| / |yTrue_ij| -> [0, inf]

    or

        - score_ij = |yPred_ij| -> [0, inf] if yTrue_ij == 0

    #### 2 Get Average ARE

        - <score> = MEAN(score_array)

    #### 3 Convert to return in range [0, 1]

        - RAE = e^(-<score>)
    """

    # Get locations of zeros and all else
    zeroLocs = np.where(yTrue == 0)
    nonZeroLocs = np.where(yTrue != 0)

    # Get scores form zero locations and non-zero locations
    # if len(zeroLocs[0]) > 0:
    #     score_zeros = np.mean(np.abs(yPred[zeroLocs]))
    # else:
    #     score_zeros = 0

    # if len(nonZeroLocs[0]) > 0:
    #     score_nonzeros = np.mean(np.abs(yTrue[nonZeroLocs] - yPred[nonZeroLocs]) / np.abs(yTrue[nonZeroLocs]))
    # else:
    #     score_nonzeros = 0

    # Get score average
    # avgScore = (score_zeros + score_nonzeros) / 2
    avg_score = np.mean(np.abs(yTrue - yPred) / (np.abs(yTrue) + 1))

    # Get/return RAE
    return np.e ** (-avg_score)

def normalize(array:np.ndarray):
    """
    ## Function

    Normalizes a given array (per col.) such that each point is the z-score for the given 
    columns mean and standard deviation. The returned array is a copy.

    Columns with only two unique values are automatically converted to be just 0's and 1's

    ## Returns

    normalized_array, mean_std_data

    ## Usage

    The following should generate a normalized array where each column of the array has a
    mean of (essentially*) 0, and a standard deviation of (essentially*) 1.

    *Due to floating point errors, the values might be off by a very minimal amount

    ```
    import numpy as np
    import mcnets as mc

    # Column index to look at
    col_index = 2

    # Generate an array with 5 columns and 100 samples
    array = np.random.rand(100, 5)
    mean = np.mean(array[:, col_index])
    std  = np.std(array[:, col_index])
    print("Original array:")
    print(f"{mean = }")
    print(f"{std = }")

    # Normalize the array on a per-column basis
    norm_array, MS_data = mc.normalize(array)

    # Use a columns to prove it is normalized (mean of 0, std of 1)
    mean = np.mean(norm_array[:, col_index])
    std  = np.std(norm_array[:, col_index])
    print()
    print("Normalized array:")
    print(f"{mean = }")
    print(f"{std = }")
    ```
    """

    # dtype Check
    array = array.astype(np.float64).copy()

    # Normalize depending on if many cols or one
    means = np.mean(array, axis=0).copy()
    sdevs = np.std(array, axis=0).copy()
    ms_data = [means, sdevs]

    # Normalize data
    array = (array-means) / sdevs

    # Finish
    return array, ms_data

def denormalize(normalized_array:np.ndarray, mean_std_data):
    """
    ## Function

    Denormalizes an array that has been normalized by the normalize() function, and
    given the mean_std_data from the array's normalization process. The returned array
    is a copy.

    ## Returns

    denormalized_array

    ## Usage

    The following should generate a normalized array where each column of the array has a
    mean of (essentially*) 0, and a standard deviation of (essentially*) 1. After this, it 
    will denormalize it using this function and bring the array back to its original mean/std.

    *Due to floating point errors, the values might be off by a very minimal amount

    ```
    import numpy as np
    import mcnets as mc

    # Column index to look at
    col_index = 2

    # Generate an array with 5 columns and 100 samples
    array = np.random.rand(100, 5)
    mean = np.mean(array[:, col_index])
    std  = np.std(array[:, col_index])
    print("Original array:")
    print(f"{mean = }")
    print(f"{std = }")

    # Normalize the array on a per-column basis
    norm_array, MS_data = mc.normalize(array)

    # Use a columns to prove it is normalized (mean of 0, std of 1)
    mean = np.mean(norm_array[:, col_index])
    std  = np.std(norm_array[:, col_index])
    print()
    print("Normalized array:")
    print(f"{mean = }")
    print(f"{std = }")

    # Denormalize the array, per-column
    denorm_array = mc.denormalize(norm_array, MS_data)

    # Use a columns to prove it is no longer normalized
    mean = np.mean(denorm_array[:, col_index])
    std  = np.std(denorm_array[:, col_index])
    print()
    print("Denormalized array (Should be same as original):")
    print(f"{mean = }")
    print(f"{std = }")
    ```
    """

    # Make array copy
    denorm_arr = normalized_array.copy()

    # Get number of columns
    # if denorm_arr.ndim > 1:
    #     # Do denormalization
    #     for col in range(denorm_arr.shape[1]):
    #         denorm_arr[:, col] = (denorm_arr[:, col] * mean_std_data[col][1]) + mean_std_data[col][0]
    # else:
    #     # Do denormalization (single col)
    #     denorm_arr[:] = (denorm_arr[:] * mean_std_data[0][1]) + mean_std_data[0][0]

    return (denorm_arr*mean_std_data[1]) + mean_std_data[0]

