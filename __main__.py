import click
import numpy as np
import utils
import time


@click.command(help="set random color")
@click.option("--light",help="lsdolo",type=click.STRING)
@click.option("--mal",help="lalaasda",type=click.STRING)
def set_random_color(light,mal):
    i = 0
    while i < int(mal):
        i += 1
        value = tuple(*np.random.randint(0,128,(1,3)))
        print(value)
        utils.set_light_color([int(light)],value)
        time.sleep(1)

@click.command(help="set light")
@click.option("--light",help="lolo",type=click.STRING)
@click.option("--value",help="lala",type=click.Tuple([float,float,float]))
def set_color(light,value):
    print(value)
    utils.set_light_color([int(light)],tuple(value))


@click.command(help="set light")
@click.option("--light",help="lolo",type=click.STRING)
@click.option("--value",help="lala",type=click.STRING)
def set_light(light,value):
    utils.set_light_dimmer([int(light)],int(value))


@click.command(help="list lights")
def list_lights():
    utils.list_all_lights()


@click.group()
def cli():
    pass

cli.add_command(set_light)
cli.add_command(list_lights)
cli.add_command(set_color)
cli.add_command(set_random_color)

if __name__ == '__main__':
    cli()
