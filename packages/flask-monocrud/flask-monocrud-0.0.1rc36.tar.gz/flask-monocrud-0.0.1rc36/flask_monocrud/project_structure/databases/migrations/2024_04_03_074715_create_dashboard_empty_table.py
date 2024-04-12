"""CreateDashboardEmptyTable Migration."""

from masoniteorm.migrations import Migration


class CreateDashboardEmptyTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("dashboard") as table:
            table.increments("id")

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("dashboard")
