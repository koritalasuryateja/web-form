# ReadMe File

## Simple Search Engine Project

### Overview
This project is a basic search engine that helps find words in a set of HTML files. It uses a *Compressed Trie* to store words and *TF-IDF (Term Frequency-Inverse Document Frequency)* to rank documents based on their relevance to a user’s query. The program processes the text in HTML files, organizes the words, and allows users to search for them, showing results in order of importance.

---

### How It Works

#### 1. *Reading HTML Files*
- *What it does*: Extracts plain text and links from HTML files.
- *How it works*:
  - Uses BeautifulSoup to read the HTML structure.
  - Extracts plain text using get_text().
  - Finds all the links (from <a> tags with href attributes).
- *What it outputs*: The plain text and a list of links from each file.

#### 2. *Processing Text*
- *What it does*: Cleans and simplifies the text before storing.
- *Steps*:
  - Converts all text to lowercase to avoid case sensitivity.
  - Breaks the text into individual words (tokenization).
  - Removes common words like "the," "is," and "and" (stop words).
  - Reduces words to their root form (e.g., "running" becomes "run") using lemmatization.

#### 3. *Compressed Trie for Storing Words*
- *What it does*: Saves words and tracks which documents contain them.
- *How it works*:
  - *TrieNode*: Each node stores a character, child nodes, and the list of documents where the word is found.
  - *CompressedTrie*: Combines nodes to store words more efficiently.
- *How it is used*:
  - *Insert*: Adds a word and links it to the document where it appears.
  - *Search*: Finds which documents contain a specific word.

#### 4. *TF-IDF for Ranking*
- *What it does*: Calculates how important a word is in a document compared to all other documents.
- *How it works*:
  - *TF (Term Frequency)*: Measures how often a word appears in a single document.
  - *IDF (Inverse Document Frequency)*: Reduces importance for words that appear in many documents.
  - *TF-IDF*: Combines TF and IDF to score each word in a document.
- *How it is used*:
  - Pre-calculates scores for all documents.
  - For each query, scores are added for matching words, and documents are ranked.

#### 5. *Searching and Ranking*
- *What it does*: Finds documents that match the query and sorts them by relevance.
- *Steps*:
  - Processes the query the same way as the text in the documents.
  - Uses the trie to find documents containing the query words.
  - Ranks documents based on their TF-IDF scores.

#### 6. *Interactive Search*
- *What it does*: Allows users to search for terms and see the results.
- *How it works*:
  - Accepts queries through the console.
  - Processes the query and retrieves matching documents.
  - Shows the results in order of relevance.

---

### Key Ideas and Tools

#### Main Steps:
1. *Read HTML*: Extracts text and links from files.
2. *Process Text*: Tokenizes, removes stop words, and lemmatizes words.
3. *Use Trie*:
   - Stores words and tracks which documents contain them.
   - Finds documents for query terms.
4. *Rank with TF-IDF*: Scores and ranks documents based on how relevant they are to the query.

#### Data Structures:
1. *Compressed Trie*: Stores words and tracks which documents contain them.
2. *Dictionaries*: Used for word counts, TF-IDF scores, and results.

---

### Example
#### Input:
Query: machine learning

#### Output:
plaintext
Ranked Results:
1. Document: document1.html
2. Document: document3.html
3. Document: document2.html

