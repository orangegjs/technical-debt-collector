sequenceDiagram
    participant FR as Fund Raiser
    participant LoginPage as :LoginPage
    participant LoginController as :LoginController
    participant UserAccount as :UserAccount

    FR->>LoginPage: user enter required credentials, username and password
    FR->>LoginPage: click login button
    LoginPage->>LoginController: login(String username, String password)
    LoginController->>UserAccount: login(String username, String password)
    UserAccount-->>LoginController: return user_acc : UserAccount
    LoginController-->>LoginPage: return user_acc : UserAccount

    alt [user_acc is not NULL]
        LoginPage->>LoginPage: displayFundRaiserDashboard()
    else [user_acc is NULL]
        LoginPage->>LoginPage: displayLoginFail()
    end