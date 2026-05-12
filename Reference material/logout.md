sequenceDiagram
    participant FR as Fund Raiser
    participant LogoutPage as :LogoutPage

    FR->>LogoutPage: click logout button
    LogoutPage->>LogoutPage: logout()