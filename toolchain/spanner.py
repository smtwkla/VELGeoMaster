import click
import os
import subprocess


@click.group
def cli():
    pass

@click.command()
def build():
    click.echo("build")
    os.system("docker build -t vel_geo_master_dev .")
    os.system("docker image ls")

@click.command()
@click.option('-f', is_flag=True, help="Force recreation.")
def configurator(f):
    click.echo("configurator")
    os.system("docker compose --profile=init_bench up db redis-cache redis-queue backend configurator"
              f'{" --force-recreate" if f else ""}'
              )

@click.command()
@click.option('-f', is_flag=True, help="Force recreation.")
def create_site(f):
    click.echo("create_site")
    os.system("docker compose --profile=init_bench up db redis-cache redis-queue backend create-site"
              f'{" --force-recreate" if f else ""}'
              )

@click.command()
@click.option('-d', is_flag=True, help="Run in daemon mode.")
@click.option('-f', is_flag=True, help="Force recreation.")
def run(d,f):
    click.echo("run")
    os.system(f"docker compose up {'-d' if d else ''}"
              f'{" --force-recreate" if f else ""}'
              )

@click.command()
@click.option('-v', is_flag=True, help="Remove container volumes.")
def stop(v):
    click.echo("stop")
    os.system(f"docker compose down {'-v' if v else ''}")

@click.command()
def bash():
    click.echo("bash")
    os.system("docker compose exec bench bash")

#REM docker run --rm -it --name customer_erp_dev -p 8000:8000 customer_erp_dev

cli.add_command(build)
cli.add_command(configurator)
cli.add_command(create_site)
cli.add_command(run)
cli.add_command(stop)
cli.add_command(bash)
if __name__ == '__main__':
    cli()