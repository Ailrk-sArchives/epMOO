"""
Some factory function to create common regex.
"""


class SearchAnchor:
    @staticmethod
    def bypass_anchor(keyword: str) -> str:
        return r'.*' + keyword + r'.*'


class SubAnchor:
    @staticmethod
    def numeric_value(keyword: str) -> str:
        return r'(\s+)[+-]?(?:[0-9]*[\.])?[0-9]+(.*{}.*)'.format(keyword)


