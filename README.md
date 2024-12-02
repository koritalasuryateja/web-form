# ReadMe File

## Search Engine Project

### Overview
This project is a simple search engine that uses a *Compressed Trie* to store and find words efficiently and *TF-IDF (Term Frequency-Inverse Document Frequency)* to rank documents based on relevance to a query. It processes text from HTML files, indexes the words, and allows users to search and retrieve ranked results.

---

### How It Works

#### 1. *Reading HTML Files*
- *What it does*: Extracts text and links from HTML files.
- *How it works*:
  - Uses the BeautifulSoup library to read the structure of the HTML.
  - Extracts plain text from the HTML using get_text().
  - Finds all hyperlinks (<a href>).
- *What it gives*: The text and list of links for each file.

#### 2. *Preparing Text*
- *What it does*: Cleans the text to make it suitable for indexing.
- *Steps*:
  - Converts the text to lowercase to avoid case sensitivity.
  - Splits the text into words (tokenization).
  - Removes common words like "the," "is," "and" (stop words).
  - Converts words to their base forms (e.g., "running" → "run") using lemmatization.

#### 3. *Compressed Trie for Indexing*
- *What it does*: Stores words and the documents they appear in, efficiently.
- *How it works*:
  - *TrieNode*: Each node in the trie stores a character, its child nodes, and a list of document IDs where the word appears.
  - *CompressedTrie*: Combines multiple nodes to store words compactly.
- *How it is used*:
  - *Insert*: Adds a word into the trie and links it to the document where it was found.
  - *Search*: Finds which documents contain a word.

#### 4. *TF-IDF for Ranking*
- *What it does*: Gives importance to words based on how frequently they appear in a document and across all documents.
- *How it works*:
  - *TF (Term Frequency)*: Measures how often a word appears in a document:
    
    TF = Word count in document/Total words in document
  
  - *IDF (Inverse Document Frequency)*: Reduces importance for words that appear in many documents:
    
    IDF = log(Total documents/Documents with the word) + 1
   
  - *TF-IDF*: Combines both to score a word's relevance:
   
    TF-IDF = TF * IDF
 
- *How it is used*:
  - Precompute TF-IDF scores for all words in all documents.
  - For each query, calculate the score for matching words and rank the documents.

#### 5. *Search and Rank*
- *What it does*: Searches for documents that match the query and sorts them by relevance.
- *Steps*:
  - Processes the query using the same text preparation steps.
  - Uses the trie to find documents containing the query words.
  - Ranks the documents using TF-IDF scores.

#### 6. *Interactive Search*
- *What it does*: Lets the user type a query and shows ranked results.
- *How it works*:
  - Accepts input in the console.
  - Processes the query, finds results, and displays the ranked list of documents.

---

### Key Concepts and Tools

#### Algorithms:
1. *HTML Parsing*: Extracts text and links from files.
2. *Text Cleaning*: Prepares text by tokenizing, removing stop words, and lemmatizing.
3. *Trie Operations*:
   - Add words to the trie with their document references.
   - Search for words to find matching documents.
4. *TF-IDF Scoring*: Ranks documents based on the relevance of words in the query.

#### Data Structures:
1. *Compressed Trie*: Efficient for storing and searching words.
2. *Dictionaries*: Used for storing word counts, TF-IDF scores, and intermediate results.

