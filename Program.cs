using System;
using System.Net.Http;
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

        static async void Bot_OnMessage(object sender, MessageEventArgs e) {
            Catfact catfact = new Catfact();
            var url = "https://cat-fact.herokuapp.com/facts";
            Console.WriteLine($"Created at {url}");
            if (e.Message.Text != null)
            {
                Console.WriteLine($"Received a text message in chat {e.Message.Chat.Id}.");
                var text = e.Message.Text;
                var reply = "";
                if (text == "/joke"){
                    reply = "this is a joke";
                }
                else{
                    reply = "hello";
                }
                await botClient.SendTextMessageAsync(
                chatId: e.Message.Chat,
                text: reply
                );  
            }
        }

        // static async Task<Catfact> GetCatfactAsync(string path){
        //     var catfact = "";
        //     HttpResponseMessage response = await client.GetAsync(path);
        //     if(response.IsSuccessStatusCode){
        //         catfact = await response.Content.ReadAsStringAsync();
        //     }
        //     return Console.WriteLine(catfact);
        // }
    }
}