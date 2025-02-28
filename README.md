# Purchase Assistant - API Chatbot

This project implements a **shopping assistant** based on the OpenAI API, designed to interact with users and answer product-related queries. Its functionality includes:

- Retrieving detailed product information.
- Checking product stock availability.
- Listing all available products.
- Testing for functionalities.

---

## **1. Technologies Used**

- **Language:** Python 3.11
- **AI Assistant:** OpenAI API
- **Testing Framework:** pytest
- **Mocking:** unittest.mock
- **Dependency Manager:** pip
- **Testing Strategy:** Automated with pytest and mocks

---

## **2. Installation and Setup**

### **2.1. Clone the Repository**

```sh
 git clone https://github.com/EmmanuelMPJ/assistance.git
 cd assistance
```

### **2.2. Create and Activate a Virtual Environment**

```sh
python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate    # On Windows
```

### **2.3. Install Dependencies**

```sh
pip install -r requirements.txt
```

### **2.4. Configure OpenAI API Key**

Before running the assistant, create a .env file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## **3. Using the Assistant**

To start the assistant, run:

```sh
python app.py
```

The user can interact with the assistant via the console.

---

## **4. Project Structure**

```
assistance-main/
│── app.py
│── catalog.json
│── report.html
│── requirements.txt
└── tests/
    ├── _init_.py
    ├── conftest.py
    ├── test_catalog.py
    ├── test_complete_interaction.py
    ├── test_get_all_products.py
    ├── test_get_product_info.py
    └── test_get_product_stock.py
```

---

## **5. Improvements needed for testing**

The assistant originally contained an unencapsulated `while True:` loop, making it difficult to capture terminal output for testing purposes and import the app since this runs the code and therefore the infinite loop.  
To improve testability, this loop was encapsulated like this: 

```python
if __name__ == "__main__":
    while True:
      ...
```

---

## **6. Testing and Validation**

The project includes automated tests to ensure proper functionality.

### **6.1. Run Unit Tests**

```sh
pytest tests/ --verbose
```

### **6.2. Main Test Cases**

| ID   | Test Case                                     | Input                  | Expected Output                                     |
|------|----------------------------------------------|------------------------|-----------------------------------------------------|
| TC01 | Validate catalog loading                     | `catalog.json` file    | Product list loaded without errors                 |
| TC02 | Retrieve existing product info              | "Laptop"              | "The product is Laptop with description: [Description] and price: [Price]." |
| TC03 | Retrieve non-existent product info          | "TabletXYZ"           | "Product not found."                              |
| TC04 | Retrieve product info from empty catalog    | "Laptop"              | "Product not found."                              |
| TC05 | Check stock availability                    | "Laptop"              | "The product Laptop is in stock with availability: 10." |
| TC06 | Check stock for non-existent product        | "TabletXYZ"           | "Product not found."                              |
| TC07 | Check stock in empty catalog                | "Laptop"              | "Product not found."                              |
| TC08 | List all products for catalog with length 2 | -                      | Correct product names listed                       |
| TC09 | List all products for catalog with length 3 | -                      | Correct product names listed                       |
| TC10 | List products from empty catalog            | -                      | "" (Empty output)                                 |
| TC11 | Assistant handles empty input               | ""                     | Prompts user for valid input                       |
| TC12 | Assistant handles special characters        | "~*^"                  | Handles input properly                            |
| TC13 | Assistant gives correct response for valid input | "I want to buy a Laptop" | Responses match "assistant > i'm searching..." |


### **6.3. Generate test report**

A summary test report can be generated using the following command.

```sh
pytest --html=report.html --self-contained-html
```

It will generate a .html that can be opened on the browser, and it will desplay something like this:

### **6.4. Running tests evidence**

when running the tests through the terminal something like the following should display:


---

## **7. Test result Summary**

The test suite ran multiple cases to validate the assistant's behavior. The majority of the tests **passed successfully**, but one test case **failed** due to an issue when handling an empty input string (`""`).  

### **📌 Key Observations:**  
👉 **Most tests passed**, confirming that catalog loading, product retrieval, and stock checks work correctly.  
👉 **One test failed** (`test_complete_interaction[""-expected_patterns2]`), revealing an issue when an empty string is provided as input.  

### **🛑 Failed Test Analysis:**  
The failing test case expected the assistant to return a message indicating an incomplete or cut-off input, matching one of these patterns:  
```python
[
    r"It (seem(s)*|look(s)*) like",
    r"message.*(incomplete|cut)",
    r"provide.*details",
]
```
However, instead of handling the empty input gracefully, the application raised a `BadRequestError` from OpenAI's API:  
```sh
Error code: 400 - {'error': {'message': 'Message content must be non-empty.', 'type': 'invalid_request_error', 'param': 'content', 'code': None}}
```
This suggests that the assistant does not properly handle empty input before sending it to OpenAI’s API.  

### **⚠️ Potential Intermittent Failures:**  
The test case `test_complete_interaction` also includes two other scenarios:  
```sh
"I want to buy a Laptop"
"~*^"
```
These tests **could fail intermittently** depending on OpenAI’s response. Since the assistant relies on dynamic AI-generated outputs, the expected patterns might not always match, causing occasional test failures.  

### **🛠️ Suggested Fix:**  
To avoid this issue, the assistant should **validate user input before sending it to OpenAI**. Specifically:  
- Ensure `user_input` is not empty before making an API request.  
- Provide a default response when an empty input is detected, instead of relying on OpenAI's API to handle it.  

### 📌 **Next Steps:** 
Review and implement input validation to handle empty messages properly and improve test stability. Additionally, these tests can be integrated into CI/CD pipelines to automatically validate each code change against the entire system, minimizing the risk of errors. Lastly, it would be beneficial to test the data types of each field in the catalog. 🚀

---

## **8. Autor**

[<img src="https://avatars.githubusercontent.com/u/168949963?v=4" width=115><br><sub>Emmanuel Paternina</sub>](https://github.com/EmmanuelMPJ)

---

