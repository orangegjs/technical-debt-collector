sequenceDiagram
    participant FR as Fund Raiser
    participant Page as : UpdateFRAPage
    participant Ctrl as : UpdateFRAController
    participant FRA as : FRA

    FR->>Page: update editable field<br />and click update
    Page->>Page: validateEnteredData(FRA activity)

    alt [entered data is invalid]
        Page->>Page: displayInputErrorMessage()
    else [entered data is valid]
        Page->>Ctrl: updateFRA(FRA activity)
        Ctrl->>FRA: updateFRA(FRA activity)
        FRA-->>Ctrl: return result: boolean
        Ctrl-->>Page: return result: boolean
        Page->>Page: displayUpdateSuccess()
    end