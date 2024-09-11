# Writing Clear Instructions

1. **Include details in queries**: Provide important context and specifics to get more relevant answers.

2. **Adopt personas**: Use the system message to specify a persona for the model to use in replies.

3. **Use delimiters**: Employ delimiters like quotes or tags to clearly indicate distinct parts of the input.

4. **Specify steps**: Write out steps explicitly for complex tasks to make them easier for the model to follow.

5. **Provide examples**: Demonstrate the desired output style through examples when it's difficult to describe explicitly.

6. **Specify output length**: Ask for outputs of a given target length in terms of words, sentences, paragraphs, or bullet points.

# Providing Reference Text

1. **Answer using references**: Instruct the model to use provided information to compose its answer.

2. **Cite from references**: Request that the model add citations to its answers by referencing passages from provided documents.

# Splitting Complex Tasks

1. **Use intent classification**: Identify the most relevant instructions for a user query to handle different cases efficiently.

2. **Summarize long conversations**: For lengthy dialogues, summarize or filter previous parts to maintain context within limits.

3. **Recursive summarization**: Summarize long documents piecewise and construct a full summary recursively for extensive content.

# Giving Models Time to Think

1. **Work out solutions first**: Instruct the model to reason from first principles before concluding to improve accuracy.

2. **Use inner monologue**: Hide the model's reasoning process using structured formats for parsing before presenting to the user.

3. **Check for missed information**: Ask the model if it missed anything on previous passes to ensure comprehensive responses.

# Using External Tools

1. **Embeddings-based search**: Implement efficient knowledge retrieval using embeddings to find relevant information dynamically.

2. **Code execution**: Use code execution for accurate calculations or to call external APIs when needed.

3. **Access specific functions**: Utilize the Chat Completions API to give models access to specific functions for enhanced capabilities.

# Testing Changes Systematically

1. **Evaluate with gold-standard answers**: Compare model outputs to known correct answers to assess performance accurately.