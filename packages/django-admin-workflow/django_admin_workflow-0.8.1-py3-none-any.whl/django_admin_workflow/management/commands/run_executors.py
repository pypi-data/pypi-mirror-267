from time import sleep

from django.core.management import BaseCommand
from django_admin_workflow.management.commands._private import get_target_ctype, get_fields_model

class Command(BaseCommand):
    help = "Run executor(s) typically with cron"
    def create_parser(self, prog_name, subcommand, **kwargs):
        return super().create_parser(prog_name, subcommand,
            usage="%(prog)s -e app_label.executor_name [-m app_label.model_name ...]\
            \n                  [-p space] [-s status] [-c nb_seconds] [options]",
            **kwargs)

    def add_arguments(self, parser):
        parser.add_argument("-e", "--executors", metavar="app_label.executor_name", nargs="*",
                            required=True, help="executor(s) selection")
        parser.add_argument("-m", "--models", metavar="app_label.model_name", nargs="*",
                            required=False, help="model(s) to process")
        parser.add_argument("-p", "--space", nargs=1,
                            required=False, help="filter on space")
        parser.add_argument("-s", "--status", nargs=1,
                            required=False, help="filter on status")
        parser.add_argument("-c", "--cron-simul", metavar="period", nargs=1, type=int,
                            required=False, help="interactive mode with a period in seconds")

    def handle(self, executors, models=None, status=None, space=None, cron_simul=None, *args, **options):
        if status:
            status = status[0]
        if  space:
            space = space[0]
        ctype_model, wf_ready, _, _ = get_target_ctype(models)
        if not wf_ready:
            print ("error model", ctype_model)
            return
        ctype_exe, wf_ready, _, _ = get_target_ctype(executors)
        if wf_ready:
            print ("error executor", ctype_exe)
            return
        if ctype_model.app_label != ctype_exe.app_label:
            print ("WARNING: executor app and worflow model app are different",
                   ctype_exe.app_label, ctype_model.app_label)

        if cron_simul:
            while True:
                self._run(ctype_exe, ctype_model, status, space)
                sleep(cron_simul[0])
        else:
            self._run(ctype_exe, ctype_model, status, space)

    def _run(self, ctype_exe, ctype_model, status, space):
        print("run",ctype_exe, ctype_model, status, space)
        Exec = ctype_exe.model_class()
        if 0 < Exec.objects.filter(running=True, status=status, space=space).count():
            print("previous still running. exit")
            return
        inst_exec = Exec.objects.create(status=status, space=space)
        qs = None
        if ctype_model: qs = ctype_model.model_class().objects
        if qs and status: qs = qs.filter(status=status)
        if qs and space: qs = qs.filter(space=space)
        if qs and status == None and space == None: qs = qs.all()
        print("launch exec run qs=", qs, "status", status)
        inst_exec.run_(status, qs)




