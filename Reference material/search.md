sequenceDiagram
    participant FR as Fund Raiser
    participant Page as : SearchFRAPage
    participant Ctrl as : SearchFRAController
    participant FRA as : FRA

    FR->>Page: input keyword and click search
    Page->>Ctrl: searchFRA(String keyword)
    Ctrl->>FRA: searchFRA(String keyword)
    FRA-->>Ctrl: return List<FRA>
    Ctrl-->>Page: return List<FRA>

    alt [result_list.size() != 0]
        Page->>Page: displayFRAFound(List<FRA> result_list)
    else [result_list.size() == 0]
        Page->>Page: displayFRANotFound()
    end