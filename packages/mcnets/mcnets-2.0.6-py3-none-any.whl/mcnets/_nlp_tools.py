import numpy as np
import main as mc

def import_text(file_names:list):
    doc_text = ['' for _ in range(len(file_names))]
    for i, doc in enumerate(file_names):
        for line in doc.readlines():
            # Remove \n at ends of lines
            line = line.replace('\n', '')

            # Append to overall text
            doc_text[i] += line.lower()
            doc_text[i] += ' '

    # Symbols to clean up
    remove = ['`', '~', '#', '$', '%', '\\', '|', '"', "'", '/']
    spaces = ['@', '_', '<', '>']

    # Add specific labels from context of symbols
    pauses = ['(', ')', "{", "}", "[", "]", ':', ';', ',', '-',]
    sentence_ends = ['.', '?', '!',]
    ands = ['&',]
    math = ['+', "=", '^', '*',]

    PAUSE_LABEL = ' PAUSE '
    END_SENTENCE_LABEL = ' STOP '
    AND_LABEL = ' and '
    MATH_LABEL = ' MATH '

    # Loop to alter and clean text
    for i in range(len(doc_text)):
        # Remove various symbols
        for bit in remove:
            doc_text[i] = doc_text[i].replace(bit, '')

        # Remove/replace symbols that likely require a space
        for bit in spaces:
            doc_text[i] = doc_text[i].replace(bit, ' ')

        # Replace symbols associated with a pause with the pause label
        for bit in pauses:
            doc_text[i] = doc_text[i].replace(bit, PAUSE_LABEL)

        # Replace symbols associated with a sentence end with the sentence end label
        for bit in sentence_ends:
            doc_text[i] = doc_text[i].replace(bit, END_SENTENCE_LABEL)

        # Replace symbols associated with a pause with the pause label
        for bit in ands:
            doc_text[i] = doc_text[i].replace(bit, AND_LABEL)

        # Replace symbols associated with a pause with the pause label
        for bit in math:
            doc_text[i] = doc_text[i].replace(bit, MATH_LABEL)


    # Remove any double spaces from putting together lines + get tokens/words
    words = [[] for _ in range(len(file_names))]
    NUMBER_LABEL = 'NUM'
    VARIABLE_LABEL = 'ALNUM'
    UNKNOWN_LABEL = 'UNKNWN'
    for i in range(len(doc_text)):
        # Reduce mega spaces (This can be optimized for sure!)
        while '  ' in doc_text[i]:
            doc_text[i] = doc_text[i].replace('  ', ' ')
            doc_text[i] = doc_text[i].replace('  ', ' ')

        # Tokenize
        words[i] = doc_text[i].split()

        # Replace numeric type parts
        for wi, word in enumerate(words[i]):
            # Replace all numbers with proper label
            if word.isnumeric():
                words[i][wi] = NUMBER_LABEL

            # Replace all (probably) variables / other garbage with this
            if word.isalnum() ^ word.isalpha():
                words[i][wi] = VARIABLE_LABEL

            # Replace all other weird symbols
            elif not word.isalpha():
                words[i][wi] = UNKNOWN_LABEL
    return words

def words_to_vec(words:list):
    """Converts a list containing lists of the split document
    words to a vector array"""
    # Get unique words
    unique = set(['', ' '])
    for doc_words in words:
        unique.update(set(doc_words))

    # Get word DF
    docfreq = {word:0 for word in unique}
    for doc_words in words:
        for uword in set(doc_words):
            docfreq[uword] += 1

    # Get word TF
    counts = {word:0 for word in unique}    
    for doc_text in words:
        for doc_word in doc_text:
            counts[doc_word] += 1

    # Get word tfidf
    tfidf = {word: (f/(df+1)+1)/5 if len(word)<=3 else (f/(df+1)+1) for word, f, df in zip(docfreq.keys(), counts.values(), docfreq.values())}

    ## ===== Embedding ===== ##

    # Define ndim of a single word vector
    # dim 1-100: word_count / (top_n_word_count + 1)
    # dim 101-200: word_doc_freq / (top_n_word_doc_freq + 1)
    # dim 201-300: word_tfidf / (top_n_word_tfidf + 1)
    # dim 301-400: (times word neighbored top_n word) / (top_n_word_count + 1)
    # dim 401-426: count of letters a-z
    # dim 427: word's tfidf value
    WORD_VEC_SIZE = 427

    # Get top 100 words (via tfidf)
    top_tfidf = tfidf.copy()
    top_tfidf = [(val, word) for val, word in zip(tfidf.values(), tfidf.keys())]
    top_tfidf.sort(reverse=True)
    top_words = [top[1] for top in top_tfidf[:100]]

    # Get neighbor values for ALL words (get just unique values later)
    word_neighbor_counts = {word1:{word2:0 for word2 in unique} for word1 in unique}
    for doc_words in words:
        for i, word in enumerate(doc_words):
            # Get current neighbor info
            left_3 = doc_words[i-3] if i >= 3 else None
            left_2 = doc_words[i-2] if i >= 2 else None
            left_1 = doc_words[i-1] if i >= 1 else None
            right_1 = doc_words[i+1] if i <= len(doc_words)-2 else None
            right_2 = doc_words[i+2] if i <= len(doc_word)-3 else None
            right_3 = doc_words[i+3] if i <= len(doc_word)-4 else None

            # Assemble neighbors by distance
            neighbors_1 = [left_1, right_1]
            neighbors_2 = [left_2, right_2]
            neighbors_3 = [left_3, right_3]

            # Add scores
            for neighbor_word in neighbors_1:
                if neighbor_word != None:
                    word_neighbor_counts[word][neighbor_word] += 1
            
            for neighbor_word in neighbors_2:
                if neighbor_word != None:
                    word_neighbor_counts[word][neighbor_word] += 0.5

            for neighbor_word in neighbors_3:
                if neighbor_word != None:
                    word_neighbor_counts[word][neighbor_word] += 0.333

    ## Making word vectors ##
    # Generate blank vectors
    all_word_vectors = np.zeros((len(unique), WORD_VEC_SIZE))

    # Setup initial values
    letters_ord = [*range(ord('a'), ord('z')+1)]
    for i, (word_f, word_df, word_tfidf, word) in enumerate(zip(counts.values(), docfreq.values(), tfidf.values(), unique)):
        # Start counts
        all_word_vectors[i, :100] = word_f

        # Start doc freqs
        all_word_vectors[i, 100:200] = word_df

        # Start tfidfs
        all_word_vectors[i, 200:300] = word_tfidf

        # Neighbor counts
        all_word_vectors[i, 300:400] = [word_neighbor_counts[word][tword] for tword in top_words]

        # Letter counts
        for li, letter in enumerate(letters_ord):
            all_word_vectors[i, 400+li] += word.count(chr(letter))
        all_word_vectors[i, 400:426] /= len(word)+1

        # Word's tfidf
        all_word_vectors[i, -1] = word_tfidf

    # 'Normalize' The main dims using the about counts
    all_word_vectors[:, :100] /= [counts[word] for word in top_words]
    all_word_vectors[:, 100:200] /= [docfreq[word] for word in top_words]
    all_word_vectors[:, 200:300] /= [tfidf[word] for word in top_words]
    all_word_vectors[:, 300:400] /= [counts[word] for word in top_words]

    return {'wordvecs':all_word_vectors, 'tf':counts, 'df':docfreq, 'tfidf':tfidf, 'unique':unique, 'wv':{w:v for w, v in zip(unique, all_word_vectors)}}

def index_to_word(unique:set, index):
    """Returns the words of the indicies given"""
    if type(index) != list:
        return list(unique)[index]
    else:
        return [list(unique)[i] for i in index]

def nearest_vec_ind(word_vec:np.ndarray, all_word_vectors:np.ndarray, num_nearest=10):
    """Gets the indicies of the nearest vectors from the given one"""
    nearest = []
    diffs = np.sum((all_word_vectors-word_vec)**2, axis=1)
    for n in range(num_nearest):
        index = np.where(diffs == np.min(diffs))[0][0]
        nearest.append(index)
        diffs[index] = np.inf
    return nearest

def nearest_vec_word(unique, word_vec:np.ndarray, all_vecs):
    """Gets the nearest word according to vector distance. Will return a
    word from the known library if given its vector."""
    return list(unique)[nearest_vec_ind(word_vec=word_vec, all_word_vectors=all_vecs, num_nearest=1)[0]]

def word_to_vec(unique, all_word_vectors, word:str):
    return all_word_vectors[list(unique).index(word)]

def softmax(x:np.ndarray, axis=0):
    # Go through cols
    return np.exp(x)/np.sum(np.exp(x), axis=axis)

def softlimit(x:np.ndarray):
    return np.abs(x)**0.5 * np.tanh(x)

class AttentionModel:
    def __init__(self, wv_size:int=427, q_dim:int=100, nn_layers:int=1, nn_height:int=25,
                 nn_activation:callable=lambda x: np.maximum(0, x)) -> None:
        """Device for learning from and using a word vector database
        
        `wv_size`:
            - Number of dimensions the given word vectors have
        
        `q_dim`:
            - Number of dimensions to use for the query space
            - This should be lower than wv_size

        `nn_layers`:
            - Number of hidden layers to use for the neural network
            that reads and adjusts the reembedded word vectors

        `nn_activation`:
            - Activation to use for the neural network hidden layers
        """
        # Dimension space
        self.q_dim = q_dim
        self.sdq = self.q_dim**0.5

        # Attention Query/Key/Value matricies
        self.Wq = (np.random.random((wv_size, self.q_dim)) - 0.5)
        self.Wk = (np.random.random((wv_size, self.q_dim)) - 0.5)

        self.Wv1 = (np.random.random((wv_size, self.q_dim)) - 0.5)
        self.Wv2 = (np.random.random((self.q_dim, wv_size)) - 0.5)

        # Neural network stuff
        nn_sizes = [wv_size] + [nn_height]*nn_layers + [wv_size]
        self.nn_weights = [np.random.random((s1, s2))-0.5 for s1, s2 in zip(nn_sizes[:-1], nn_sizes[1:])]
        self.nn_biases = [np.random.random(s2)-0.5 for s2 in nn_sizes[1:]]
        self.nn_activation = nn_activation

        # Fit stuff
        self.params = [self.Wq, self.Wk, self.Wv1, self.Wv2] + self.nn_weights

    def _calculate_attention(self, word_vecs:np.ndarray):
        # Get queries/keys
        Q = np.dot(word_vecs, self.params[0])
        K = np.dot(word_vecs, self.params[1])

        # QK^T / d_k^0.5
        out = np.dot(Q, K.T) / self.sdq**2

        # Scaling ???? (makes everything too close to equal in probs array)
        # out -= np.min(out)
        # out = out / np.max(out) if np.max(out) != 0 else out

        # # Masking ??
        out = softlimit(out)

        # Masking ?????
        out += -np.tril(np.ones(out.shape)*1e3, -1)
        out = softmax(out)

        # Value matrix
        V = np.dot(word_vecs, np.dot(self.params[2], self.params[3]))

        # Final formulaeaeaeaeaea
        return np.dot(out, V)
    
    def _calculate_neural(self, word_vecs:np.ndarray):
        """Adjusts the reembedded word vectors via a neural network"""
        # Iterate through weights; add biases
        if len(self.nn_weights) == 0:
            return 0
        
        for W, B in zip(self.params[4:], self.nn_biases):
            word_vecs = self.nn_activation(np.dot(word_vecs, W) + B)
        return word_vecs
    
    def predict(self, word_vecs:np.ndarray):
        # Attention head
        out = word_vecs.copy() + self._calculate_attention(word_vecs)

        # Neural Network layer
        out = self._calculate_neural(out)
        return np.average(out, axis=0)
    
    def _score(self, X:list, Y:list, scoring='r2'):
        """For use in .fit only; not to be manually called"""
        return np.average([mc.score_model(self, x, y, method=scoring) for x, y in zip(X, Y)])
    
    def word_predict(self, words:'list[str]', word2vec:dict):
        model_vec = self.predict(np.array([word2vec[wi] for wi in words]))
        return nearest_vec_word(list(word2vec.keys()), model_vec, np.array(list(word2vec.values())))
    
    def fit(self, word_vecs:np.ndarray, max_iter=100, max_extension=10, learning_rate=1, 
            use_fine_tune=False, scoring='r2'):
        """Makes N-1 training samples from the sequence of N word 
        vectors given."""

        # Make training data
        # Gonna have to handle multiple X/Y sets at once now!
        # Just make adjustments and get average score across all sets
        X = [word_vecs[:i-1].copy() for i in range(2, len(word_vecs))]
        Y = [word_vecs[i-1].copy() for i in range(2, len(word_vecs))]

        # Adjust data from max extension
        X = X[np.maximum(0, len(X)-1-max_extension):]
        Y = Y[np.maximum(0, len(X)-1-max_extension):]

        # Get inital stuff
        learning_rate = learning_rate
        crnt_score = self._score(X, Y, scoring=scoring)

        # Training
        k = 0
        k_last_improved = 0
        for itr in range(max_iter):
            # Loop through params to adjust
            for i, param in enumerate(self.params):
                # Adjust param by rows if 2D
                if param.ndim >= 2 and use_fine_tune:
                    for ri, row in enumerate(param):
                        # Adjust param
                        diff = learning_rate*2*(np.random.random(row.shape) - 0.5)
                        self.params[i][ri] += diff
                        adj_score = self._score(X, Y, scoring=scoring)

                        # Check for improvement
                        if adj_score > crnt_score:
                            crnt_score = adj_score
                            k_last_improved = k
                        else:
                            self.params[i][ri] -= diff

                        if k-k_last_improved > 10:
                            learning_rate /= 2
                            k_last_improved = k

                        print(f"Epoch #{k} | Score: {crnt_score:.6f} | Leraning Rate: {learning_rate:.6f}   ", end='\r')
                        k += 1

                # 1D param adjustment or big 2D adjustment
                else:
                    # Adjust param
                    og_param = self.params[i].copy()
                    self.params[i] = learning_rate*2*(np.random.random(param.shape) - 0.5)

                    # Check for improvement
                    adj_score = self._score(X, Y, scoring=scoring)
                    if adj_score > crnt_score:
                        crnt_score = adj_score
                        k_last_improved = k
                    else:
                        self.params[i] = og_param

                    if k-k_last_improved > 10:
                        learning_rate /= 2
                        k_last_improved = k

                    print(f"Epoch #{k} | Score: {crnt_score:.6f} | Leraning Rate: {learning_rate:.6f}   ", end='\r')
                    k += 1
