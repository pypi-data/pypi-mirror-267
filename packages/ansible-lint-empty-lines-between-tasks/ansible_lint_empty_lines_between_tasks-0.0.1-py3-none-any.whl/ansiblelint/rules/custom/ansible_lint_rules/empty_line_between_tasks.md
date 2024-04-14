# Empty Line Between Tasks
This rule identifies consecutive tasks that don't have an empty line between them for better readability.

## Problematic Code
```yaml
---
- name: Problematic example
  hosts: localhost
  tasks:
    - name: Echo a message
      ansible.builtin.cmd: echo hello
      changed_when: false
    - name: Echo another message # <-- no newline before this task
      ansible.builtin.cmd: echo world
      changed_when: false

```
## Correct Code
```yaml
---
- name: Problematic example
  hosts: localhost
  tasks:
    - name: Echo a message
      ansible.builtin.cmd: echo hello
      changed_when: false

    - name: Echo another message
      ansible.builtin.cmd: echo world
      changed_when: false

```

These problems can be automatically fixed using `--fix`.
