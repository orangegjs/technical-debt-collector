sequenceDiagram
    participant FR as Fund Raiser
    participant Page as :SuspendFRAPage
    participant Ctrl as :SuspendFRAController
    participant FRA as :FRA

    FR->>Page: update status to "Suspended" and click confirm
    FR->>Page: click "confirm"
    Page->>Ctrl: suspendFRA (int fraID)
    Ctrl->>FRA: suspendFRA (int fraID)
    FRA-->>Ctrl: return suspendResult: boolean
    Ctrl-->>Page: return suspendResult: boolean

    alt [Fund Raiser clicks "confirm"]
        alt [suspendResult == True]
            Page->>Page: displaySuspendSuccess()
        else [suspendResult == False]
            Page->>Page: displaySuspendFail()
        end
    else [Fund Raiser clicks "cancel"]
        Page->>Page: return
end