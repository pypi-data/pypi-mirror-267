
class SampleClass():
    """
    Some summary with link https://www.microsoft.com
    """
    def dummy_summary(self):
        """
        This is a content issue link [microsoft](https://www.microsoft.com)
        We should not generate nested parenthesis causing docs validation warnings
        """
        pass

    def dummy_summary2(self):
        """
        This isn't a content issue link (https://www.microsoft.com)
        Should expect a transformed Markdown link.
        """
        pass

    pass
    