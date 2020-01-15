"""
${comment}

Author: ${author}
Create Date: ${create_date}

Notice: Migration auto-generated using dbgrate

"""

def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}