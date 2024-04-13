class printer:
    def __init__(self):
        self.a  = 1


    def viterbi(self):
        print('''
                        # import library
            import pandas as pd
            import numpy as np
            import nltk
            
            nltk.download('punkt')
            nltk.download('averaged-perceptron-tagger')
            
            text = "Aligned to the"
            
            words = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(words)
            
            vocab = list(set(words))
            unique_tags =  list(set([val for key,val in pos_tags]))
            len(vocab),len(unique_tags)
            
            V = len(vocab)
            T = len(unique_tags)
            
            def transition_prob(t1,t2,data=pos_tags):
                tags = [val for key,val in data]
                t1_count = tags.count(t1)
                t1_t2_count = 0
                for i in range(len(tags)-1):
                    if tags[i] == t1 and tags[i+1]==t2:
                        t1_t2_count += 1
                return t1_count,t1_t2_count
            
            def emission_prob(t1,w1,data=pos_tags):
                tags = [pair for pair in data if pair[1]==t1]
                t1_count = len(tags)
                word = [key for key,val in tags if key==w1]
                w1_count = len(word)
                return w1_count,t1_count
            
            def calculate_start_prob(data=pos_tags,tags=unique_tags):
                full_stop_index = []
                for i , pair in enumerate(pos_tags):
                    if pair[0]=='.':
                        full_stop_index.append(i)
                start_index = [0]
                for idx in full_stop_index:
                    if idx+1 < len(data):
                        start_index.append(idx+1)
                start_prob = {}
                start_tags = [data[idx][1] for idx in start_index]
                for tag in tags:
                    start_prob[tag] = round(start_tags.count(tag)/len(start_index),4)
            
                return start_prob
            
            start_prob = calculate_start_prob()
            
            start_prob
            
            emission_prob_mat = np.zeros((V,T))
            transition_prob_mat = np.zeros((T,T))
            for i,tag1 in enumerate(unique_tags):
                for j , tag2 in enumerate(unique_tags):
                    t1_t2 , t1 = transition_prob(tag1,tag2)
                    transition_prob_mat[i][j]= round((t1_t2+1)/(t1+T),4)
            
            for i,word in enumerate(vocab):
                for j,tag in enumerate(unique_tags):
                    w,t = emission_prob(tag,word)
                    emission_prob_mat[i][j] = round((w+1)/(t+V),4)
            
            emission_df = pd.DataFrame(emission_prob_mat,columns=unique_tags,index=vocab)
            transition_df = pd.DataFrame(transition_prob_mat,columns=unique_tags,index=unique_tags)
            
            emission_df.head()
            
            transition_df.head()
            
            emission_df.loc[vocab[0],unique_tags[0]]
            
            def viterbi(start_prob,emission_prob,transition_prob,obs_states,hidden_states):
                v = [{}]
                for i in start_prob:
                    v[0][i] = [round(start_prob[i]*emission_prob.loc[obs_states[0],i],4),None]
                for i in range(1,len(obs_states)):
                    v.append({})
                    for tag in hidden_states:
                        prev_prob = [v[i-1][t][0] * transition_df.loc[t,tag] for t in hidden_states]
                        max_prob = max(prev_prob)
                        prev_tag = hidden_states[prev_prob.index(max_prob)]
                        v[i][tag]=[max_prob*emission_df.loc[obs_states[i],tag],prev_tag]
                return v
            
            obs_states = "Aligned to the vision of the department"
            obs_states = obs_states.split()
            v = viterbi(start_prob,emission_df,transition_df,obs_states,unique_tags)
            
            path = []
            i = len(obs_states)-1
            curr_path = max(v[-1],key = lambda k : v[-1][k][0])
            path.append(curr_path)
            #v[word-1][curr_path][1]
            while i >= 0 :
                curr_path = v[i][curr_path][1]
                path.append(curr_path)
                i -= 1
            
            path = np.flip(path)
            print(path)
        ''')

    def skipgram(self):
        print('''
                import numpy as np
        import string
        from nltk.corpus import stopwords 
        
        def softmax(x):
            """Compute softmax values for each sets of scores in x."""
            e_x = np.exp(x - np.max(x))
            return e_x / e_x.sum()
        
        class word2vec(object):
            def __init__(self):
                self.N = 10
                self.X_train = []
                self.y_train = []
                self.window_size = 2
                self.alpha = 0.001
                self.words = []
                self.word_index = {}
        
            def initialize(self,V,data):
                self.V = V
                self.W = np.random.uniform(-0.8, 0.8, (self.V, self.N))
                self.W1 = np.random.uniform(-0.8, 0.8, (self.N, self.V))
                
                self.words = data
                for i in range(len(data)):
                    self.word_index[data[i]] = i
        
            
            def feed_forward(self,X):
                self.h = np.dot(self.W.T,X).reshape(self.N,1)
                self.u = np.dot(self.W1.T,self.h)
                #print(self.u)
                self.y = softmax(self.u) 
                return self.y
                
            def backpropagate(self,x,t):
                e = self.y - np.asarray(t).reshape(self.V,1)
                # e.shape is V x 1
                dLdW1 = np.dot(self.h,e.T)
                X = np.array(x).reshape(self.V,1)
                dLdW = np.dot(X, np.dot(self.W1,e).T)
                self.W1 = self.W1 - self.alpha*dLdW1
                self.W = self.W - self.alpha*dLdW
                
            def train(self,epochs):
                for x in range(1,epochs):	 
                    self.loss = 0
                    for j in range(len(self.X_train)):
                        self.feed_forward(self.X_train[j])
                        self.backpropagate(self.X_train[j],self.y_train[j])
                        C = 0
                        for m in range(self.V):
                            if(self.y_train[j][m]):
                                self.loss += -1*self.u[m][0]
                                C += 1
                        self.loss += C*np.log(np.sum(np.exp(self.u)))
                    print("epoch ",x, " loss = ",self.loss)
                    self.alpha *= 1/( (1+self.alpha*x) )
                    
            def predict(self,word,number_of_predictions):
                if word in self.words:
                    index = self.word_index[word]
                    X = [0 for i in range(self.V)]
                    X[index] = 1
                    prediction = self.feed_forward(X)
                    output = {}
                    for i in range(self.V):
                        output[prediction[i][0]] = i
                    
                    top_context_words = []
                    for k in sorted(output,reverse=True):
                        top_context_words.append(self.words[output[k]])
                        if(len(top_context_words)>=number_of_predictions):
                            break
            
                    return top_context_words
                else:
                    print("Word not found in dictionary")
                
                def preprocessing(corpus):
            stop_words = set(stopwords.words('english')) 
            training_data = []
            sentences = corpus.split(".")
            for i in range(len(sentences)):
                sentences[i] = sentences[i].strip()
                sentence = sentences[i].split()
                x = [word.strip(string.punctuation) for word in sentence
                                            if word not in stop_words]
                x = [word.lower() for word in x]
                training_data.append(x)
            return training_data
            
        
        def prepare_data_for_training(sentences,w2v):
            data = {}
            for sentence in sentences:
                for word in sentence:
                    if word not in data:
                        data[word] = 1
                    else:
                        data[word] += 1
            V = len(data)
            data = sorted(list(data.keys()))
            vocab = {}
            for i in range(len(data)):
                vocab[data[i]] = i
            
            #for i in range(len(words)):
            for sentence in sentences:
                for i in range(len(sentence)):
                    center_word = [0 for x in range(V)]
                    center_word[vocab[sentence[i]]] = 1
                    context = [0 for x in range(V)]
                    
                    for j in range(i-w2v.window_size,i+w2v.window_size):
                        if i!=j and j>=0 and j<len(sentence):
                            context[vocab[sentence[j]]] += 1
                    w2v.X_train.append(center_word)
                    w2v.y_train.append(context)
            w2v.initialize(V,data)
        
            return w2v.X_train,w2v.y_train 
                
            corpus = ""
            corpus += "The earth revolves around the sun. The moon revolves around the earth"
            epochs = 1000
            
            training_data = preprocessing(corpus)
            w2v = word2vec()
            
            prepare_data_for_training(training_data,w2v)
            w2v.train(epochs) 
            
            print(w2v.predict("around",3)) ''')
    def word2vec(self):
        print('''
            import numpy as np

            # Generate some sample data skipgram this is easy
            corpus = ["I like playing football with my friends",
                      "My friends enjoy playing football too",
                      "Football is a fun game",
                      "We play football every weekend"]

            # Tokenize the corpus
            words = []
            for sentence in corpus:
                words.extend(sentence.lower().split())

            vocab = set(words)
            word2id = {word: i for i, word in enumerate(vocab)}
            id2word = {i: word for word, i in word2id.items()}
            vocab_size = len(vocab)

            # Generate skip-grams
            window_size = 2
            skipgrams = []
            for sentence in corpus:
                words = sentence.lower().split()
                for i, target_word in enumerate(words):
                    for j in range(max(0, i - window_size), min(len(words), i + window_size + 1)):
                        if i != j:
                            context_word = words[j]
                            skipgrams.append((word2id[target_word], word2id[context_word]))

            # Define the model parameters
            embedding_dim = 100
            learning_rate = 0.01
            num_epochs = 10  # Adjust this as needed

            # Initialize word embeddings randomly
            W = np.random.uniform(-1, 1, (vocab_size, embedding_dim))

            # Training loop
            for epoch in range(num_epochs):
                total_loss = 0
                np.random.shuffle(skipgrams)
                for target_id, context_id in skipgrams:
                    target_embedding = W[target_id]
                    context_embedding = W[context_id]

                    # Calculate the dot product of target and context embeddings
                    score = np.dot(target_embedding, context_embedding)

                    # Apply sigmoid function to get probabilities
                    pred = 1 / (1 + np.exp(-score))

                    # Calculate the loss
                    loss = -np.log(pred)

                    # Update the embeddings using gradient descent
                    grad = pred - 1
                    W[target_id] -= learning_rate * grad * context_embedding
                    W[context_id] -= learning_rate * grad * target_embedding

                    total_loss += loss

                print(f'Epoch {epoch + 1}, Loss: {total_loss / len(skipgrams)}')

            import numpy as np

            def train_cbow(corpus, vocab_size, embedding_dim, window_size, learning_rate, num_epochs):
                W = np.random.uniform(-1, 1, (vocab_size, embedding_dim))
                word_to_id = {word: i for i, word in enumerate(vocab)}
                id_to_word = {i: word for word, i in word_to_id.items()}

                for epoch in range(num_epochs):
                    total_loss = 0
                    np.random.shuffle(corpus)
                    for i, target_word in enumerate(corpus):
                        context = []
                        for j in range(i - window_size, i + window_size + 1):
                            if i != j and j >= 0 and j < len(corpus):
                                context.append(corpus[j])
                        if context:
                            target_id = word_to_id[target_word]
                            context_ids = [word_to_id[word] for word in context]
                            target_embedding = W[target_id]
                            context_embeddings = [W[context_id] for context_id in context_ids]

                            pred = np.mean(context_embeddings, axis=0)
                            loss = -np.log(sigmoid(np.dot(pred, target_embedding)))
                            total_loss += loss

                            grad = sigmoid(np.dot(pred, target_embedding)) - 1
                            for context_id in context_ids:
                                W[context_id] -= learning_rate * grad * pred
                            W[target_id] -= learning_rate * grad * target_embedding

                    print(f'Epoch {epoch + 1}, Loss: {total_loss / len(corpus)}')

                return W, word_to_id, id_to_word

            def sigmoid(x):
                return 1 / (1 + np.exp(-x))

            # Example usage:
            corpus = ["I like playing football with my friends",
                      "My friends enjoy playing football too",
                      "Football is a fun game",
                      "We play football every weekend"]

            words = []
            for sentence in corpus:
                words.extend(sentence.lower().split())

            vocab = set(words)
            vocab_size = len(vocab)
            embedding_dim = 100
            window_size = 2
            learning_rate = 0.01
            num_epochs = 10

            W, word_to_id, id_to_word = train_cbow(words, vocab_size, embedding_dim, window_size, learning_rate, num_epochs)

            print("Word Embeddings:")
            print(W)

            # Inspect the embedding for a specific word
            word_to_inspect = "football"
            if word_to_inspect in word_to_id:
                word_id = word_to_id[word_to_inspect]
                embedding = W[word_id]
                print(f"Embedding for '{word_to_inspect}':")
                print(embedding)
            else:
                print(f"'{word_to_inspect}' not found in the vocabulary.")

            # Save word embeddings to a file if needed
            np.savetxt("word_embeddings.txt", W)''')

        return None

