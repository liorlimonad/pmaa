#!/usr/bin/env python3
"""
Enrich OCEL event log with task objects derived from commit messages.

Reads: commitizen.json
Writes: commitizen_task_objects.json

Flow:
1. Parse conventional commit messages to extract task metadata
2. Create task objects for each commit
3. Link tasks to commits (realizes relationship)
4. Link tasks to events via the commits they reference
"""

import json
import re

# Conventional commit pattern
CONVENTIONAL_PATTERN = re.compile(
    r'^(?P<type>\w+)'
    r'(?:\((?P<scope>[^)]+)\))?'
    r'(?:!)?'
    r':\s*(?P<description>.+)$'
)

TASK_MAPPING = {
    "feat": "feature_development",
    "fix": "defect_resolution",
    "refactor": "code_restructuring",
    "docs": "documentation",
    "test": "quality_assurance",
    "build": "build_engineering",
    "ci": "deployment_engineering",
    "chore": "maintenance",
    "perf": "performance_improvement",
    "style": "formatting"
}


def get_attr(attr_list, name):
    """Get an attribute value by name from a list of {name, value} dicts."""
    for attr in attr_list:
        if attr["name"] == name:
            return attr.get("value")
    return None


def set_attr(attr_list, name, value):
    """Set or update an attribute in a list of {name, value} dicts."""
    if value is None:
        return
    
    for attr in attr_list:
        if attr["name"] == name:
            attr["value"] = value
            return
    
    attr_list.append({"name": name, "value": value})


def parse_commit(message):
    """Parse a conventional commit message, return task metadata or None."""
    if not message:
        return None
    
    m = CONVENTIONAL_PATTERN.match(message.strip())
    if not m:
        return None
    
    t = m.group("type").lower()
    
    return {
        "task_type": t,
        "task_scope": m.group("scope"),
        "task_description": m.group("description"),
        "task_semantic_class": TASK_MAPPING.get(t, "other")
    }


def enrich_ocel_with_tasks(ocel, message_attr="commit_message"):
    """
    Enrich OCEL with tasks derived from commit messages.
    
    Creates task objects, links them to commits and events.
    """
    
    # Ensure task object type exists
    obj_types = ocel.setdefault("objectTypes", [])
    if not any(t["name"] == "task" for t in obj_types):
        obj_types.append({
            "name": "task",
            "attributes": [
                {"name": "task_type", "type": "string"},
                {"name": "task_scope", "type": "string"},
                {"name": "task_description", "type": "string"},
                {"name": "task_semantic_class", "type": "string"}
            ]
        })
    
    objects = ocel.get("objects", [])
    events = ocel.get("events", [])
    
    new_tasks = []
    commit_to_task = {}
    enriched_commits = 0
    
    # Process commits: extract tasks, create task objects
    for obj in objects:
        if obj.get("type") != "commit":
            continue
        
        attr_list = obj.setdefault("attributes", [])
        message = get_attr(attr_list, message_attr)
        parsed = parse_commit(message)
        
        if not parsed:
            continue
        
        # Add task attributes to commit
        for k, v in parsed.items():
            set_attr(attr_list, k, v)
        
        # Create task object
        task_id = f"task_{len(new_tasks)}"
        task_obj = {
            "id": task_id,
            "type": "task",
            "attributes": [
                {"name": "task_type", "value": parsed["task_type"]},
                {"name": "task_scope", "value": parsed["task_scope"]},
                {"name": "task_description", "value": parsed["task_description"]},
                {"name": "task_semantic_class", "value": parsed["task_semantic_class"]}
            ],
            "relationships": []
        }
        new_tasks.append(task_obj)
        
        # Link commit to task
        rels = obj.setdefault("relationships", [])
        rels.append({"objectId": task_id, "qualifier": "realizes"})
        
        commit_to_task[obj["id"]] = task_id
        enriched_commits += 1
    
    # Link tasks to events
    events_with_tasks = 0
    for event in events:
        event_rels = event.get("relationships", [])
        
        # Find which commits this event references
        commit_ids = {rel["objectId"] for rel in event_rels if rel["objectId"] in commit_to_task}
        
        # Add the realized tasks to the event
        for commit_id in commit_ids:
            task_id = commit_to_task[commit_id]
            if not any(rel["objectId"] == task_id for rel in event_rels):
                event_rels.append({"objectId": task_id, "qualifier": "realizes"})
                events_with_tasks += 1
    
    # Add new tasks to objects
    objects.extend(new_tasks)
    
    print(f"Enriched {enriched_commits} commits with task metadata")
    print(f"Created {len(new_tasks)} task objects")
    print(f"Linked {events_with_tasks} event-task relationships")
    
    return ocel


if __name__ == "__main__":
    # Load input
    with open("commitizen.json") as f:
        ocel = json.load(f)
    
    # Enrich
    ocel = enrich_ocel_with_tasks(ocel)
    
    # Save output
    with open("commitizen_task_objects.json", "w") as f:
        json.dump(ocel, f, indent=2)
    
    print("\nOutput saved to commitizen_task_objects.json")
