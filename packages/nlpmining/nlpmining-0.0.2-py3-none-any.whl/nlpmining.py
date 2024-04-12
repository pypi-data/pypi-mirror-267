class printer:
    def __init__(self):
        self.a  = 1
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

        def hmm(self):
            print('''import pandas as pd
                import numpy as  np

                df=pd.read_csv("/content/NER dataset.csv")

                nltk.download('punkt')
                nltk.download('averaged_perceptron_tagger')

                df=pd.read_csv("/content/amazon_cells_labelled.csv")

                df['So there is no way for me to plug it in here in the US unless I go by a converter.'][10]

                import nltk
                from nltk.tokenize import word_tokenize

                # Sample text
                text = "This is a sample sentence for POS tagging."
                temp=[]
                for i in df['So there is no way for me to plug it in here in the US unless I go by a converter.']:
                    word = word_tokenize(i)
                    temp.append(word)
                words=[]
                for i in temp:
                  # words.append("<s>")
                  for j in i:
                    words.append(j)
                  # words.append('<E>')
                # Tokenize the text into words
                # words = word_tokenize(text)
                # Perform POS tagging
                pos_tags = nltk.pos_tag(words)

                # Print the POS tagged result
                print(pos_tags)

                """# Count of tags and words"""

                d={}
                for i in pos_tags:
                  if i in d:
                    d[i]+=1
                  else:
                    d[i]=1

                d

                d_tag_tag = {}

                for sentence in df['So there is no way for me to plug it in here in the US unless I go by a converter.']:
                    temp_sen = "s " + sentence + " E"
                    words = word_tokenize(temp_sen)

                    pos_tags_tag = nltk.pos_tag(words)
                    if ("s", pos_tags_tag[1][1]) not in d_tag_tag:
                        d_tag_tag["s", pos_tags_tag[1][1]] = 1
                    else:
                        d_tag_tag["s", pos_tags_tag[1][1]] += 1

                    for i in range(2, len(pos_tags_tag) - 1):
                        if (pos_tags_tag[i-1][1], pos_tags_tag[i][1]) not in d_tag_tag:
                            d_tag_tag[pos_tags_tag[i-1][1], pos_tags_tag[i][1]] = 1
                        else:
                            d_tag_tag[pos_tags_tag[i-1][1], pos_tags_tag[i][1]] += 1

                    if (pos_tags_tag[len(pos_tags_tag)-1][1], 'E') not in d_tag_tag:
                        d_tag_tag[pos_tags_tag[len(pos_tags_tag)-1][1], 'E'] = 1
                    else:
                        d_tag_tag[pos_tags_tag[len(pos_tags_tag)-1][1], 'E'] += 1
                    # print(d_tag_tag)


                # Print the transition probability dictionary
                print(d_tag_tag)

                """# unique tags in array and count of tags in dictionary"""

                arr_tags=set()
                d_tags={}
                for i in range(len(pos_tags)):
                  if pos_tags[i][1] not in d_tags:
                    d_tags[pos_tags[i][1]]=1
                  else:
                    d_tags[pos_tags[i][1]]+=1
                  arr_tags.add(pos_tags[i][1])
                arr_tags=list(arr_tags)

                """# Unique words in array"""

                arr_words=set()
                for i in range(len(pos_tags)):
                  arr_words.add(pos_tags[i][0])
                arr_words=list(arr_words)

                """# Emission matrix"""

                # Create a DataFrame with arr_tags as columns and arr_words as row names
                # def emission():
                df_emission = pd.DataFrame(index=arr_words, columns=arr_tags)

                # Fill the DataFrame with 1 to indicate presence of tag for each word
                for i in arr_tags:
                  for j in arr_words:
                    if (j, i) not in d:
                            df_emission[i][j] = 0
                    else:
                            df_emission[i][j]=d[(j,i)]/d_tags[i]

                # Fill NaN values with 0 to indicate absence of tag
                df_emission = df_emission.fillna(0)

                # Display the DataFrame
                print(df_emission)

                df_emission

                arr_new=arr_tags
                arr_new.append('s')
                arr_new.append("E")

                arr_new

                """# Transition matrix"""

                df_transition = pd.DataFrame(index=arr_new, columns=arr_new)

                df_transition = df_transition.fillna(0)

                for tag1 in arr_new:
                    for tag2 in arr_new:
                        if (tag1, tag2) in d_tag_tag:
                            if tag1 =='<s>' or tag2 =='<E>':
                                  df_transition.loc[tag1, tag2] = d_tag_tag[tag1, tag2] / len(df)
                            else:
                                  df_transition.loc[tag1, tag2] = d_tag_tag[tag1, tag2] / d_tags[tag2]

                print(df_transition)

                df_transition['#']

                """# HMM"""

                text="He was very impressed when going from the original battery to the extended battery"
                # text="s "+text+" E"



                words = word_tokenize(text)

                # def viterbi():
                p={}
                for i in words:
                  for j in arr_tags:
                    # print(j)
                      p[('s',j,i)]=df_transition[j]['s']*df_emission[j][i]

                import numpy as np

                def viterbi(words, arr_tags, df_transition, df_emission):
                    # Initialize the Viterbi matrix and backpointer matrix
                    viterbi_matrix = np.zeros((len(arr_tags), len(words)))
                    backpointer = np.zeros((len(arr_tags), len(words)), dtype=int)

                    # Initialize the first column of the Viterbi matrix using initial probabilities
                    for i, tag in enumerate(arr_tags):
                        viterbi_matrix[i, 0] = df_transition[tag]['s'] * df_emission[tag][words[0]]
                        backpointer[i, 0] = -1  # No previous state

                    # Fill the rest of the Viterbi matrix
                    for t in range(1, len(words)):
                        for i, tag in enumerate(arr_tags):
                            max_prob = 0
                            max_index = 0
                            for j, prev_tag in enumerate(arr_tags):
                                prob = viterbi_matrix[j, t-1] * df_transition[tag][prev_tag] * df_emission[tag][words[t]]
                                if prob > max_prob:
                                    max_prob = prob
                                    max_index = j
                            viterbi_matrix[i, t] = max_prob
                            backpointer[i, t] = max_index

                    # Find the best path by backtracking
                    best_path = []
                    max_prob = 0
                    max_index = 0
                    for i, tag in enumerate(arr_tags):
                        if viterbi_matrix[i, len(words)-1] > max_prob:
                            max_prob = viterbi_matrix[i, len(words)-1]
                            max_index = i
                    best_path.append(max_index)
                    for t in range(len(words)-1, 0, -1):
                        max_index = backpointer[max_index, t]
                        best_path.insert(0, max_index)
                    return best_path

                # Usage
                best_path = viterbi(words, arr_tags, df_transition, df_emission)
                # print(best_path)
                best_path_tags = [arr_tags[i] for i in best_path]
                print(best_path_tags)

                pos_tags = nltk.pos_tag(words)

                pos_tags

                arr_tags

                ''')

    def viterbi(self):
        print('''
        text = """
        Aligned to the vision of the department - Stay Ahead and Be Relevant, the Department of Applied Mathematics and Computational Sciences has introduced various programmes predicting the demands of this ever-changing world. It is also the largest department in PSG College of Technology and its breadth and scale bring unique advantage in terms of bridging the demand of industry ready professionals through state-of-the-art programmes run by the department. Graduate teaching provides a strong foundation in Mathematics and Computer science and also exposes students to the latest research and developments. The department offers 5 graduate programmes and one undergraduate programme.
        The five year integrated M.Sc Software Systems (erstwhile Software Engineering) programme, offered since 1997, caters to the human resource requirement of leading software industries across the globe. The programme has been designed to meet the challenging needs of the industry, by ensuring a good understanding of the software design process and to develop resilient applications using state-of-the art technologies.
        The five year integrated M.Sc Theoretical Computer Science is yet another innovative programme offered since 2007 has been well received by the R&D divisions of software industries and top notch research institutions for higher education across the globe.
        In the new era of Big Data, M.Sc Data Science was introduced during 2015 to solve the exponential growth and curse of dimensionality in giant databases accumulated by the industries. The programme has been designed to meet the current demands in the industry and to create pioneering experts in the field of data science.
        The five-year integrated M.Sc. Cyber Security programme was started in the year 2020, the first of its kind in India aims to prepare students with the technical knowledge and skills needed to protect and defend computer systems and networks. The programme has a strong and wide technical base and internship programs which are the most critical aspects to a good cyber security education.
        The M.Sc Applied Mathematics programme was offered by the department since 1975 to acquaint the students with various principles of Mathematics and apply to all relative fields of science, technology and management. This programme is also designed to expose the students to the development and applications of software, catering to the needs of the industries and R&D Sector.
        To meet the requirements of IT field, the department offers an undergraduate programme B.Sc Computer Systems & Design (erstwhile Computer Technology) since 1985. This programme emphasizes development of programming skills, understanding system design tools and technologies for effective problem solving.
        The Department has over 60 faculty members with a wide range of research specialties, spanning Mathematical Modelling, Topology, Epidemic Modelling, Graph Algorithms, Applied Machine learning to Cybersecurity. Their publications, fellowships and project funding strengthen the recognition of our department as a powerhouse of research as well as excellent teaching.
        """

        import numpy as np
        import pandas as pd
        import nltk

        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

        words = nltk.word_tokenize(text)

        pos_tags = nltk.pos_tag(words)

        for word, pos_tag in pos_tags:
            print(f"{word}: {pos_tag}")

        V = set()
        for i in pos_tags:
          V.add(i[0])
        print(V)

        T = set()
        for i in pos_tags:
          T.add(i[1])
        print(T)

        t = len(T)
        v = len(V)
        emission_prob = np.zeros((v, t))
        transition_prob = np.zeros((t, t))

        emission_prob.shape

        def tpm(t2, t1, data = pos_tags):
            tags = [pair[1] for pair in data]
            count_t1 = len([t for t in tags if t==t1])
            count_t2_t1 = 0
            for index in range(len(tags)-1):
                if tags[index]==t1 and tags[index+1] == t2:
                    count_t2_t1 += 1
            return (count_t2_t1, count_t1)

        for i, t1 in enumerate(list(T)):
            for j, t2 in enumerate(list(T)):
                transition_prob[i, j] = tpm(t2, t1)[0]/tpm(t2, t1)[1]

        transition_prob_df = pd.DataFrame(transition_prob, columns = list(T), index = list(T))

        transition_prob_df

        def emissionprob(word, tag, data = pos_tags):
            tag_list = [pair for pair in data if pair[1]==tag]
            count_tag = len(tag_list)
            emission_list = [pair[0] for pair in tag_list if pair[0]==word]
            count_emission = len(emission_list)

            return (count_emission, count_tag)

        for i, word in enumerate(list(V)):
            for j, tag in enumerate(list(T)):
                emission_prob[i, j] = emissionprob(word, tag)[0]/emissionprob(word, tag)[1]

        emission_prob_df = pd.DataFrame(emission_prob, columns = list(T), index = list(V))

        emission_prob_df

        def calculate_start_prob(pos_tags):
            start_prob = {}
            total_sentences = len(pos_tags)

            # Count occurrences of each POS tag at the beginning of sentences
            for tags in pos_tags:
                start_tag = tags[0]
                start_prob[start_tag] = start_prob.get(start_tag, 0) + 1

            # Normalize counts to obtain probabilities
            for tag in start_prob:
                start_prob[tag] /= total_sentences

            return start_prob

        start_prob = calculate_start_prob(pos_tags)

        def viterbi(obs, states, start_prob, trans_prob, emit_prob):
            V = [{}]
            path = {}
            obs = list(obs)
            states  = list(states)

            # Initialize base cases (t = 0)
            for state in states:
                V[0][state] = start_prob[state] * emit_prob.loc[state, obs[0]]
                path[state] = [state]

            # Run Viterbi for t > 0
            for t in range(1, len(obs)):
                V.append({})
                new_path = {}

                for state in states:
                    # Find the maximum probability and corresponding state at t - 1
                    (prob, prev_state) = max((V[t - 1][prev_state] * trans_prob.loc[prev_state, state] *
                                              emit_prob.loc[state, obs[t]], prev_state) for prev_state in states)
                    # Update Viterbi path and probability
                    V[t][state] = prob
                    new_path[state] = path[prev_state] + [state]

                path = new_path

            # Find the maximum probability at the last observation
            (prob, state) = max((V[len(obs) - 1][final_state], final_state) for final_state in states)

            return path[state]''')