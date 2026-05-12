sequenceDiagram
    participant FR as Fund Raiser
    participant Page as :CreateFRAPage
    participant Ctrl as :CreateFRAController
    participant FRA as :FRA

    FR->>Page: new FRA details
    FR->>Page: Fund Raiser clicks submit

    alt if FRA exists in the system
        Page->>Ctrl: validateRepeatFRA(fraName: String, fraDescription: String, fraGoalAmount: decimal, fraStartDate: date, fraEndDate: date, fraStatus: String, fraCategory: FRACategory, fraOwner: UserAccount)
        Ctrl-->>Page: displayDuplicateFRA()
    else if FRA does not exist in the system
        Note over FR,FRA: [if FRA does not exist in the system]
        Page->>Ctrl: createFRA(fraName: String, fraDescription: String, fraGoalAmount: decimal, fraStartDate: date, fraEndDate: date, fraStatus: String, fraCategory: FRACategory, fraOwner: UserAccount)
        Ctrl->>FRA: 
        FRA-->>Ctrl: return creationResult: boolean
        Ctrl-->>Page: return creationResult: boolean

        alt creationResult == true
            Page->>Page: displayFRACreatedSuccess()
        else creationResult == false
            Page->>Page: displayFRACreatedFail()
        end
    end