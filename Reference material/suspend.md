sequenceDiagram
    participant FR as Fund Raiser
    participant Page as :SuspendFRAPage
    participant Ctrl as :SuspendFRAController
    participant FRA as :FRA

    FR->>Page: select FRA status to "suspend" <br />and click confirm
    Page->>Ctrl: updateFRAStatus(int FRA_ID, boolean status)
    Ctrl->>FRA: updateFRAStatus(int FRA_ID, boolean status)
    FRA-->>Ctrl: return FRA
    Ctrl-->>Page: return FRA
    Page->>Page: displayFRA()