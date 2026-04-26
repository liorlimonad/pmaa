## OBJECT-CENTRIC PROCESS DESCRIPTION: ISSUE_REPORTER

The **issue_reporter** role represents the part of the software development process where users initiate, shape, and follow the lifecycle of issues. This role is centered on creating issue objects, engaging with them through comments and mentions, and participating in the surrounding collaboration network of users and issue-related events. In object-centric terms, the role is not only about opening issues, but also about continuously attaching user interactions to those issues as they evolve, are reviewed, resolved, reopened, or closed.

---

## 1. Process Overview

The issue_reporter role is responsible for starting issue-based work and sustaining communication around those issues throughout their lifecycle. The process typically begins when an issue is **created**, after which the reporter or other involved users may **comment**, **mention** colleagues, **subscribe** to updates, or otherwise interact with the issue as it develops.

A major part of this role’s behavior is collaborative coordination. Issue reporters do not act in isolation; they create and maintain links between **issue objects** and **user objects** through activities such as commenting, mentioning, subscribing, and being assigned or requested for review. The role also appears in later-stage issue handling, where issues are **closed**, **reopened**, or otherwise updated as work progresses.

Overall, this role supports the intake, communication, and follow-up of issues across the development lifecycle, ensuring that problem reports remain visible, discussed, and actionable.

---

## 2. Main Activities

### Issue initiation and setup
- **created**: This is the starting point of the process, where a new issue is introduced into the system. It establishes the issue object and connects it to the creating user.
- **labeled / unlabeled**: These activities classify or reclassify the issue, helping to organize and prioritize reported work.
- **assigned / unassigned**: These events connect or disconnect responsibility for the issue to a user, indicating who is expected to act on it.
- **milestoned / demilestoned**: These activities link the issue to a milestone, showing planning or release alignment.
- **issue_type_added**: This refines the issue’s categorization.

### Collaboration and communication
- **commented**: The most frequent activity, used to add discussion, clarification, updates, or follow-up information to an issue.
- **mentioned**: Indicates that a user was referenced in relation to the issue, often to draw attention or request input.
- **subscribed / unsubscribed**: These activities manage who receives updates about the issue.
- **pinned / unpinned**: These are less frequent but indicate emphasis or prioritization in the issue context.
- **locked**: Suggests that discussion on the issue has been restricted, often to control communication.

### Review and resolution-related handling
- **review_requested**: A user is asked to review or inspect the issue-related work. This activity strongly connects the issue to a requested reviewer user.
- **reviewed**: Indicates that review has taken place, usually as part of evaluating the issue or associated work.
- **ready_for_review**: Marks the issue or related work as ready for formal review.
- **convert_to_draft / converted_to_discussion**: These activities indicate changes in the issue’s state or format, often reflecting a shift between active work and discussion-oriented handling.

### Closure and lifecycle completion
- **closed**: Marks the issue as resolved or completed.
- **reopened**: Indicates that a previously closed issue has been brought back into active consideration.
- **converted_to_discussion**: Suggests a transition from a more formal issue state into a discussion-oriented object or state.

### Structural and reference-related updates
- **renamed**: The issue’s title or identifier is changed, typically for clarity or correction.
- **cross_referenced / referenced**: These activities connect the issue to other issues, commits, or related work items, showing traceability and dependency.
- **head_ref_force_pushed / base_ref_force_pushed / head_ref_deleted / head_ref_restored / base_ref_changed / base_ref_deleted**: These are more technical lifecycle events, usually associated with linked development work. In the issue reporter context, they indicate that the issue is connected to an evolving implementation or change context.
- **connected**: Establishes a relationship between objects, often linking the issue to another relevant entity.

---

## 3. Object Interactions

The process is strongly object-centric, with the issue reporter role interacting mainly with **issue** and **user** objects.

### Interaction with issues
The issue is the central object in this process. Nearly every activity is anchored to an issue timeline event, meaning the role contributes to the issue’s history through creation, discussion, status changes, and closure. Activities such as **commented**, **mentioned**, **subscribed**, **closed**, and **reopened** all directly update the issue object and reflect its evolving state.

### Interaction with users
User objects are the second major object type. The role interacts with users in several ways:
- as the **actor user** performing the activity,
- as the **created user** when an issue is opened,
- as the **requested_reviewer user** when review is requested.

This shows that the process is not just about issue state transitions, but also about managing participation among people. For example, **review_requested → requested_reviewer user** creates a direct coordination link between an issue and a specific user, while **commented → actor user** and **mentioned → actor user** show who contributed to the issue conversation.

### Meaning of the interactions
These interactions indicate that the issue reporter role acts as a coordination hub:
- it creates and updates issue objects,
- it binds users to issues through discussion and review,
- it maintains visibility and accountability through subscriptions and assignments,
- and it supports traceability by linking issues to related events and references.

Although the log contains only two object types, the events show rich multi-object behavior, especially where one activity simultaneously involves an issue and one or more users.

---

## 4. Process Flow Patterns

The most common flow begins with **created**, followed by one or more communication and coordination activities such as **commented**, **mentioned**, and **subscribed**. This reflects an iterative issue-handling pattern in which the issue is opened, discussed, and monitored.

A very prominent pattern is repeated communication:
- **commented → commented**
- **commented → mentioned**
- **mentioned → subscribed**

This suggests that issue handling is highly conversational and collaborative, with users repeatedly adding context and drawing others into the issue.

Another important pattern is review and closure:
- **review_requested → review_requested**
- **reviewed → merged**
- **merged → closed**
- **commented → closed**

This shows that issues often move through a review-oriented path before being finalized. The repeated **review_requested → review_requested** sequence indicates that review requests may be reassigned, repeated, or updated multiple times for the same issue.

Closure is often followed by technical cleanup or follow-up actions:
- **closed → head_ref_deleted**

This suggests that once the issue is resolved, related development references are removed or cleaned up.

There are also occasional reversal patterns:
- **reopened**
- **convert_to_draft**
- **review_request_removed**

These indicate that the process is not strictly linear. Issues may return to active work, lose review status, or be reclassified as the situation changes.

---

## 5. Key Characteristics

- **Highly communication-driven**: The dominant activity is **commented**, showing that the role is centered on discussion and coordination.
- **Strong user involvement**: Many activities directly connect issues to users, especially through comments, mentions, subscriptions, and review requests.
- **Iterative and non-linear**: Repeated events such as **review_requested → review_requested** and **commented → commented** show that issues often undergo multiple rounds of interaction.
- **Issue-centric collaboration**: The issue is the main object around which all activity is organized, making the process highly traceable at the issue level.
- **Lifecycle spanning from creation to closure**: The role participates across the full issue lifecycle, from opening and discussion to resolution and possible reopening.
- **Coordination rather than execution**: Compared with implementation-focused roles, this role primarily facilitates communication, visibility, and follow-up.

---

## Concise Business Interpretation

The issue_reporter role contributes to the software development lifecycle by ensuring that problems, requests, and discussions are formally captured and actively managed. It initiates issue records, keeps them visible through comments and mentions, and supports collaboration by linking the right users to the right issues at the right time. In business terms, this role is essential for demand intake, team coordination, and maintaining traceability from issue creation through resolution.

---

## Process Statistics

- **Total Events**: 16037
- **Total Objects**: 1863
- **Unique Activities**: 34
- **Object Types**: 2

### Activities (by frequency):
  - commented: 2900 occurrences
  - review_requested: 1639 occurrences
  - closed: 1432 occurrences
  - reviewed: 1120 occurrences
  - created: 1089 occurrences
  - mentioned: 994 occurrences
  - subscribed: 962 occurrences
  - head_ref_force_pushed: 946 occurrences
  - labeled: 891 occurrences
  - merged: 876 occurrences
  - cross_referenced: 828 occurrences
  - head_ref_deleted: 702 occurrences
  - referenced: 603 occurrences
  - unlabeled: 362 occurrences
  - renamed: 184 occurrences
  - ready_for_review: 100 occurrences
  - base_ref_changed: 76 occurrences
  - milestoned: 69 occurrences
  - base_ref_force_pushed: 68 occurrences
  - assigned: 68 occurrences
  - convert_to_draft: 48 occurrences
  - reopened: 17 occurrences
  - demilestoned: 12 occurrences
  - review_request_removed: 10 occurrences
  - base_ref_deleted: 9 occurrences
  - unassigned: 8 occurrences
  - head_ref_restored: 4 occurrences
  - issue_type_added: 4 occurrences
  - locked: 4 occurrences
  - converted_to_discussion: 4 occurrences
  - unsubscribed: 3 occurrences
  - connected: 2 occurrences
  - pinned: 2 occurrences
  - unpinned: 1 occurrences

### Object Types:
  - issue: 1436 objects
  - user: 427 objects

### Top Activity Flows:
  - review_requested → review_requested: 1055 times
  - merged → closed: 876 times
  - mentioned → subscribed: 826 times
  - commented → commented: 818 times
  - commented → mentioned: 763 times
  - closed → head_ref_deleted: 479 times
  - reviewed → merged: 452 times
  - subscribed → commented: 354 times
  - head_ref_force_pushed → head_ref_force_pushed: 302 times
  - commented → closed: 293 times

### Top Object Interactions:
  - Activity 'commented' timeline_event issue: 2900 times
  - Activity 'commented' actor user: 2900 times
  - Activity 'review_requested' timeline_event issue: 1639 times
  - Activity 'review_requested' actor user: 1639 times
  - Activity 'review_requested' requested_reviewer user: 1639 times
  - Activity 'closed' timeline_event issue: 1432 times
  - Activity 'closed' actor user: 1432 times
  - Activity 'reviewed' timeline_event issue: 1120 times
  - Activity 'reviewed' actor user: 1120 times
  - Activity 'created' created issue: 1089 times
  - Activity 'created' created user: 1089 times
  - Activity 'mentioned' timeline_event issue: 994 times
  - Activity 'mentioned' actor user: 994 times
  - Activity 'subscribed' timeline_event issue: 962 times
  - Activity 'subscribed' actor user: 962 times