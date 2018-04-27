from sportorg.core.template import get_text_from_file
from sportorg.models.memory import race

from sportorg.modules.printing.printing import print_html
from sportorg.config import template_dir
from sportorg.models.result.split_calculation import GroupSplits


class NoResultToPrintException(Exception):
    pass


class NoPrinterSelectedException(Exception):
    pass


def split_printout(result):
    person = result.person

    if not person or not person.group:
        raise NoResultToPrintException('No results to print')

    obj = race()
    printer = obj.get_setting('split_printer')
    template_path = obj.get_setting('split_template', template_dir('split', 'split_printout.html'))
    if person.group and person.group.course:
        spl = GroupSplits(race(), person.group).generate()
        # FIXME
        # template = get_text_from_file(template_path, **spl.get_dict_printout(person))
        template = ''
        if not printer:
            raise NoPrinterSelectedException('No printer selected')
        print_html(
            printer,
            template,
            obj.get_setting('print_margin_left', 5.0),
            obj.get_setting('print_margin_top', 5.0),
            obj.get_setting('print_margin_right', 5.0),
            obj.get_setting('print_margin_bottom', 5.0),
        )
