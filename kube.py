from collector.kube_api import init_kube_client, watch_nais_apps, print_event_to_console

init_kube_client()
watch_nais_apps(print_event_to_console)
