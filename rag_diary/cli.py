from logging import getLogger

from click import group, command, echo, argument, pass_context

from rag_diary.boot import boot
from rag_diary.config import Config
from rag_diary.controller import Controller


logger = getLogger(__name__)


@group()
@pass_context
def cli(ctx):
    config: Config = Config()
    controller: Controller = boot(config)
    ctx.obj = {"controller": controller}


@command()
@argument("entry")
@pass_context
def new_entry(ctx, entry: str):
    controller: Controller = ctx.obj["controller"]
    result = controller.new_entry(entry)
    logger.info(result)


@command()
@argument("query")
@pass_context
def query_db(ctx, query: str):
    controller: Controller = ctx.obj["controller"]
    result = controller.query_db(query)
    logger.info(result)


@command()
@argument("query")
@pass_context
def query_retriever_agent(ctx, query: str):
    controller: Controller = ctx.obj["controller"]
    result = controller.query_retriever_agent(query)
    logger.info(result)


cli.add_command(new_entry)
cli.add_command(query_db)
cli.add_command(query_retriever_agent)

if __name__ == "__main__":
    cli()
