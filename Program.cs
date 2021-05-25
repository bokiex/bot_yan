using System;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Telegram.Bot;
using Telegram.Bot.Args;

namespace bot_yan {

    public class Catfact{
        public string id {get;set;}
        public string text {get;set;}
    }
    class Program {
        static ITelegramBotClient botClient = new TelegramBotClient("1792786927:AAEiCd0d_2jxiGe2vCCQ9NzYOeBWmWKB6wc");
        static HttpClient client = new HttpClient();

        static void Main() {
            
            var me = botClient.GetMeAsync().Result;
            Console.WriteLine(
                $"Hello, World! I am user {me.Id} and my name is {me.FirstName}."
            );

            botClient.OnMessage += Bot_OnMessage;
            botClient.StartReceiving();

            Console.WriteLine("Press any key to exit");
            Console.ReadKey();

            botClient.StopReceiving();
        }

        static async Task<Catfact> GetFactAsync(string path){
            Catfact catfact = null;
            HttpResponseMessage response = await client.GetAsync(path);
            if (response.IsSuccessStatusCode)
            {
                catfact = await response.Content.ReadAsAsync<Catfact>();
            }
            return catfact;
        }

        static async void Bot_OnMessage(object sender, MessageEventArgs e) {
            Catfact catfact = new Catfact();
            var url = "https://cat-fact.herokuapp.com/facts";
            Console.WriteLine($"Created at {url}");
            catfact = await GetFactAsync(url);
            Console.WriteLine(catfact.text);
            if (e.Message.Text != null)
            {
                Console.WriteLine($"Received a text message in chat {e.Message.Chat.Id}.");

                await botClient.SendTextMessageAsync(
                chatId: e.Message.Chat,
                text:   "You said:\n" + e.Message.Text
                );
            }
        }
    }
}