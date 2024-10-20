import click
import os
import subprocess
import secrets
import bump_version as bv


def run_cmd(cmd):
	print(">>> " + cmd)
	os.system(cmd)


def commit_and_push():
	ver = bv.read_version()
	run_cmd(f'git commit -m "bumped to version {ver}"')
	run_cmd(f'git push origin main')


def	build_target(target):
	if target == "dev":
		click.echo("build bench container image for dev")
		os.system("docker build -t vel_geo_master_dev .")
		os.system("docker image ls")
	elif target == "base":
		click.echo("build frappe_base container image for prod")
		os.system("docker build -t frappe_base:latest --file=build/Dockerfile build")
	elif target == "app":
		click.echo("build vel_geo_master container image for prod")
		ver = bv.read_version()
		os.system(
			f"docker build --no-cache -t {secrets.APP_IMAGE_NAME}:v{ver} --file=build/Dockerfile-app "
			f'--build-arg REPO_URI="{secrets.REPO_URI}" '
			"build")


def	push_target(target):
	os.system(
		f"docker login -u {secrets.REPO_USER} -p {secrets.REPO_TOKEN} {secrets.CONTAINER_REPO_SERVER}"
	)
	if target == "base":
		click.echo("Not implemented.")
	elif target == "app":
		ver = bv.read_version()
		image_name = secrets.APP_IMAGE_NAME
		app_image_uri = secrets.APP_IMAGE_URI
		app_image_uri_with_ver = app_image_uri + ":v" + ver
		click.echo(f'Pushing to {app_image_uri_with_ver}...')
		run_cmd(f"docker image tag {image_name}:v{ver} {app_image_uri}:v{ver}")
		run_cmd(f"docker image tag {app_image_uri_with_ver} {app_image_uri}:latest")
		run_cmd(f"docker image push {app_image_uri_with_ver}")


@click.group
def cli():
	pass


@cli.command()
def bump_ver():
	bv.bump_version()


@cli.command()
def get_ver():
	click.echo(bv.read_version())


@click.command()
@click.argument('target')
def build(target):
	build_target(target)


@click.command()
@click.argument('target')
def push(target):
	push_target(target)


@click.command()
def release_app():
	bv.bump_version()
	commit_and_push()
	build_target("app")
	push_target("app")


@click.command()
@click.option('-f', is_flag=True, help="Force recreation.")
def configurator(f):
	click.echo("run configurator on dev compose stack")
	os.system(
		"docker compose --profile=init_bench up db redis-cache redis-queue backend configurator"
		f'{" --force-recreate" if f else ""}'
		)


@click.command()
@click.option('-f', is_flag=True, help="Force recreation.")
def create_site(f):
	click.echo("run create_site on dev compose stack")
	os.system(
		"docker compose --profile=init_bench up db redis-cache redis-queue backend create-site"
		f'{" --force-recreate" if f else ""}'
		)


@click.command()
@click.option('-d', is_flag=True, help="Run in daemon mode.")
@click.option('-f', is_flag=True, help="Force recreation.")
def run(d, f):
	click.echo("run dev compose stack")
	os.system(f"docker compose up {'-d' if d else ''}"
			  f'{" --force-recreate" if f else ""}'
			  )

@click.command()
def bash():
	os.system("docker compose exec bench bash")

@click.command()
def bench_start():
	os.system('docker compose exec bench bash -c "cd /home/frappe/frappe-bench; bench start"')

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
cli.add_command(bash)
cli.add_command(stop)
cli.add_command(bash)
cli.add_command(bench_start)
cli.add_command(push)
cli.add_command(get_ver)
cli.add_command(bump_ver)
cli.add_command(release_app)

if __name__ == '__main__':
	cli()
