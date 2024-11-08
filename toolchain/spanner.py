import click
import os
import subprocess
import secrets
import bump_version as bv

APP = secrets.APP


def run_cmd(cmd):
	print(">>> " + cmd)
	os.system(cmd)


def commit_and_push():
	ver = bv.read_version()
	run_cmd(f'git commit -m "bumped to version {ver}"')
	run_cmd(f'git push origin main')


def	build_target(target, n=None):
	""" builds dev image, base image or app. -n for No cache. Usage build {dev | base | app } [-n] """
	if target == "dev":
		click.echo("build bench container image for dev")
		os.system(f"docker build -t {APP}_dev -f dev_Dockerfile {'--no-cache' if n else ''} .")
		os.system("docker image ls")
	elif target == "base":
		click.echo("build frappe_base container image for prod")
		os.system(f"docker build -t frappe_base:latest --file=build/Dockerfile-base {'--no-cache' if n else ''} build")
	elif target == "app":
		click.echo(f"build {APP} container image for prod")
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

def check_if_repo_dirty():
	result = subprocess.run(
		["git", "status", "--porcelain"],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE
	)
	if result.returncode != 0:
		click.echo("Error checking Git repository status.")
		exit(1)
	if result.stdout:
		click.echo("There are uncommitted changes in the repository:")
		click.echo(result.stdout.decode("utf-8"))
		exit(1)


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
@click.option('-n', is_flag=True, help="No Cache.")
def build(target, n):
	build_target(target, n)


@click.command()
@click.argument('target')
def push(target):
	push_target(target)


@click.command()
def release_app():
	check_if_repo_dirty()
	bv.bump_version()
	commit_and_push()
	build_target("app")
	push_target("app")

@click.command()
@click.option('-d', is_flag=True, help="Run in daemon mode.")
@click.option('-f', is_flag=True, help="Force recreation.")
def run(d, f):
	click.echo("run dev compose stack")
	os.system(f"docker compose -f dev_compose.yaml -p dev_{APP} up {'-d' if d else ''}"
			  f'{" --force-recreate" if f else ""}'
			  )

@click.command()
def bash():
	os.system(f"docker compose -f dev_compose.yaml -p dev_{APP} exec bench bash")

@click.command()
def bench_build_dev():
	os.system(f'docker compose -f dev_compose.yaml -p dev_{APP} exec bench bash -c "/workspace/toolchain/dev_install.sh"')

@click.command()
def bench_start():
	os.system(f'docker compose -f dev_compose.yaml -p dev_{APP} exec bench bash -c "cd /home/frappe/frappe-bench; bench start"')

@click.command()
@click.option('-v', is_flag=True, help="Remove container volumes.")
def stop(v):
	click.echo("stop dev compose stack")
	os.system(f"docker compose -f dev_compose.yaml -p dev_{APP} down {'-v' if v else ''}")


@click.command()
def bash():
	click.echo("bash into bench container")
	os.system(f"docker compose -f dev_compose.yaml -p dev_{APP} exec bench bash")


cli.add_command(build)
cli.add_command(run)
cli.add_command(bash)
cli.add_command(stop)
cli.add_command(bash)
cli.add_command(bench_build_dev)
cli.add_command(bench_start)
cli.add_command(push)
cli.add_command(get_ver)
cli.add_command(bump_ver)
cli.add_command(release_app)

if __name__ == '__main__':
	cli()

