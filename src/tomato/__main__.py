import tomato
import click
import json

@click.command()
@click.option('--config-file', default=None, help="Path to a configuration file")
@click.option('--duration', default=tomato.Config().duration, help="Duration in minute")
@click.option('--sound', default=tomato.Config().sound, help="Path to the sound to play")
def run(config_file, duration, sound):
    root = tomato.tk.Tk()
    if config_file is not None:
      import json
      with open(config_file) as cfg:
        config = tomato.Config(**json.load(cfg))
    else:
      config = tomato.Config(duration = duration, sound = sound)
    app = tomato.Application(master=root, config = config)
    app.mainloop()

if __name__ == "__main__":
    run()
