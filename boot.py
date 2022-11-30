import supervisor

if callable(getattr(supervisor, 'set_next_stack_limit', None)):
    supervisor.set_next_stack_limit(4096 + 4096)
else:
    supervisor.runtime.next_stack_limit = 4096 + 4096
