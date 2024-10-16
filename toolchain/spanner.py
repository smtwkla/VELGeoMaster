import click
import os
import subprocess
import secrets


@click.group
def cli():
	pass

@click.command()
@click.argument('target')
def build(target):
	if target == "dev":
		click.echo("build bench container image for dev")
		os.system("docker build -t vel_geo_master_dev .")
		os.system("docker image ls")
	elif target == "base":
		click.echo("build frappe_base container image for prod")
		os.system("docker build -t frappe_base:latest --file=build/Dockerfile build")
	elif target == "app":
		click.echo("build vel_geo_master container image for prod")
		click.echo(secrets.REPO_URI)
		os.system(f"docker build -t {secrets.APP_IMAGE_NAME}:{secrets.APP_VERSION} --file=build/Dockerfile-app "
		          f'--build-arg REPO_URI="{secrets.REPO_URI}" '
		          "build")

@click.command()
@click.argument('target')
def push(target):
	os.system(f"docker login -u {secrets.REPO_USER} -p {secrets.REPO_TOKEN} {secrets.CONTAINER_REPO_SERVER}")
	if target == "base":
		click.echo("Not implemented.")
	elif target == "app":
		cmd = f"docker image tag {secrets.APP_IMAGE_NAME}:{secrets.APP_VERSION} {secrets.APP_IMAGE_URI}"
		click.echo(cmd)
		os.system(cmd)
		cmd = f"docker image push {secrets.APP_IMAGE_URI}"
		click.echo(cmd)
		os.system(cmd)

@click.command()
@click.option('-f', is_flag=True, help="Force recreation.")
def configurator(f):
	click.echo("run configurator on dev compose stack")
	os.system("docker compose --profile=init_bench up db redis-cache redis-queue backend configurator"
			  f'{" --force-recreate" if f else ""}'
			  )

@click.command()
@click.option('-f', is_flag=True, help="Force recreation.")
def create_site(f):
	click.echo("run create_site on dev compose stack")
	os.system("docker compose --profile=init_bench up db redis-cache redis-queue backend create-site"
			  f'{" --force-recreate" if f else ""}'
			  )

@click.command()
@click.option('-d', is_flag=True, help="Run in daemon mode.")
@click.option('-f', is_flag=True, help="Force recreation.")
def run(d,f):
	click.echo("run dev compose stack")
	os.system(f"docker compose up {'-d' if d else ''}"
			  f'{" --force-recreate" if f else ""}'
			  )

@click.command()
@click.option('-v', is_flag=True, help="Remove container volumes.")
def stop(v):
	click.echo("stop dev compose stack")
	os.system(f"docker compose down {'-v' if v else ''}")

@click.command()
def bash():
	click.echo("bash into bench container")
	os.system("docker compose exec bench bash")

#REM docker run --rm -it --name customer_erp_dev -p 8000:8000 customer_erp_dev

cli.add_command(build)
cli.add_command(configurator)
cli.add_command(create_site)
cli.add_command(run)
cli.add_command(stop)
cli.add_command(bash)
cli.add_command(push)
if __name__ == '__main__':
	cli()
