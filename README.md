# Single-Banking-System
Simple Banking System task made for an upskilling program for Capgemini. 


Task details:

Banking System User (Bank Manager or Customer)

  I want to Manage clients by adding, removing, and retrieving them.
Allow clients to perform transactions such as deposits and withdrawals.
Keep a record of all transactions for auditing and reference.
Prevent invalid transactions such as overdrawing or depositing negative amounts.
Generate a detailed transaction statement for each client. So that
Clients can securely manage their balances and track their transactions.
The bank can maintain accurate records of customer activities.
Errors are handled properly, ensuring a robust and reliable system.

Acceptance Criteria

Client Management

  ✅ The system allows adding new clients with a unique ID, name, and initial balance.
  
  ✅ Clients can be retrieved by their unique ID.
  
  ✅ Clients can be removed from the system when necessary.

Bank Operations

  ✅ The system maintains a list of all registered clients.
  
  ✅ It provides a method to display the balance of all clients.

Transactions
  
  ✅ Clients can deposit money into their account.
  
  ✅ Clients can withdraw money, provided they have sufficient funds.
  
  ✅ A transaction record is created for each deposit and withdrawal, capturing:

        1.Client name
        
        2.Transaction type (deposit/withdrawal)
        
        3.Amount
        
        4.Date & time

Transaction History & Statements

  ✅ Each client has a personal transaction history.
  
  ✅ Clients can generate a transaction statement showing all past transactions.

Error Handling

  ✅ Deposits of negative amounts should be rejected.
  
  ✅ Withdrawals that exceed the balance should not be allowed.
  
  ✅ The system should raise clear errors for invalid operations.

Code Quality & Structure

  ✅ Each class should be in a separate file, following a modular structure.
  
  ✅ All classes must have __repr__ and __str__ where applicable.
  
  ✅ Client balances should be managed using properties.
  
  ✅ Unique IDs must be assigned to each client for easy tracking.

Testing & Validation

  ✅ Unit tests should be written using pytest to ensure correct functionality.
