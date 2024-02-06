import discord
from discord.ext import commands
from difflib import get_close_matches
import json
from dotenv import load_dotenv
import os
from typing import Final


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.knowledge_base = self.load_knowledge_base('knowledge_base.json')

    @staticmethod
    def find_best_match(user_question: str, questions: list[str]) -> str | None:
        matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
        return matches[0] if matches else None

    @staticmethod
    def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
        for q in knowledge_base["questions"]:
            if q["question"] == question:
                return q["answer"]
        return None

    @staticmethod
    def load_knowledge_base(file_path: str) -> dict:
        try:
            with open(file_path, 'r') as file:
                data: dict = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{file_path}'.")
            
    @staticmethod
    def save_knowledge_base(file_path: str, data: dict):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        user_input = message.content.lower()

        if user_input.startswith('!join') or user_input.startswith('!leave') or user_input.startswith('!play') or user_input.startswith('!pause') or user_input.startswith('!resume') or user_input.startswith('!stop') or user_input.startswith('!kick'):
            await self.bot.process_commands(message)
            return

        if user_input.startswith('!') and not await self.bot.process_commands(message):
            question = user_input[5:].strip()
            best_match = self.find_best_match(question, [q["question"] for q in self.knowledge_base["questions"]])

            if best_match:
                answer = self.get_answer_for_question(best_match, self.knowledge_base)
                await message.channel.send(f'Bot: {answer}')
            else:
                await message.channel.send('Bot: I don\'t know the answer. Can you teach me?')

                new_answer = await self.bot.wait_for("message", check=lambda m: m.author == message.author, timeout=60)

                if new_answer.content.lower() != 'skip':
                    self.knowledge_base["questions"].append({"question": question, "answer": new_answer.content})
                    self.save_knowledge_base('knowledge_base.json', self.knowledge_base)
                    await message.channel.send('Bot: Thank you! I learned a new response!')



async def setup(bot):
    await bot.add_cog(Chat(bot))
