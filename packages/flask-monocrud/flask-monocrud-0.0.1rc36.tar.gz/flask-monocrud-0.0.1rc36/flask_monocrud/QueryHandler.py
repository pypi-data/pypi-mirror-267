from flask_orphus import orequest
from masoniteorm import Model
from masoniteorm.query import QueryBuilder
from flask_monocrud import AdminModel


class QueryHandler:
    def __init__(self, model_instance, result_set: QueryBuilder | None = None, admin_model=None):
        self.model_instance: Model = model_instance
        self.result_set: dict | Model = result_set
        self.admin_model: AdminModel = admin_model
        self.query_builder: QueryBuilder | None = None
        if self.result_set is None:
            self.result_set = self.model_instance
            if self.query_builder is None:
                self.query_builder = self.model_instance.query()
        else:
            self.query_builder = result_set.builder
            try:
                self.model_instance = result_set
            except AttributeError:
                pass

    def build_table_filters(self):
        if self.admin_model.table.filters():
            for table_filter in self.admin_model.table.filters():
                if orequest.has(table_filter.get('name')):
                    self.query_builder = self.query_builder.where(
                        lambda q: table_filter.get('query')(q)
                    )
                return self
        return self

    def build_table_tab_filters(self):
        if self.admin_model.table.tabs:
            for table_filter in self.admin_model.table.tabs():
                if orequest.has("tab_filter"):
                    if orequest.input("tab_filter") == table_filter.get('name'):
                        self.query_builder = self.query_builder.where(
                            lambda q: table_filter.get('query')(q)
                        )
                        return self
        return self

    def build_search_query(self):
        search_query: str = self.admin_model.table.search.search_query
        #print(search_query)
        initial_selects = self.model_instance.__selects__
        search_field: str | list = self.admin_model.table.search.search_field
        hybrid_searchable_fields: list = list()
        try:
            for field in self.admin_model.model_instance.get_table().__dict__():
                if field.get('searchable'):
                    searchable = field.get('searchable_fields')
                    hybrid_searchable_fields.append(field.get('name'))
                    self.query_builder.where_concat(searchable, "like", f'%{search_query}%')
        except AttributeError:
            pass

        if not isinstance(search_field, (list,)):
            search_field = [search_field]

        self.builder = self.query_builder.or_where(
            lambda q: q.where_any(search_field, "like", search_query)
        )
        self.admin_model.table.search.hybrid_search_fields = hybrid_searchable_fields
        return self

    def handle(self):
        self.build_table_filters()
        try:
            self.build_search_query()
        except AttributeError:
            pass

        self.build_table_tab_filters()
        #print(self.query_builder.to_sql())

        return self.result_set

