<h1>Transfer Reddit Subscriptions from one account to another</h1>
<i>Currently does not support > 100 subscriptions per account</i>

<h2>Setup</h2>
<ol>
	<li>Sign in to the Reddit account you want to export subscriptions from.</li>
	<li>Create a new script application. Enter 'http://127.0.0.1:3030/callback' (without quotes) as the redirect URI,</li>
	<li>Repeat this for the account you want to import subscriptions to.</li>
</ol>
<br/>
<h3>accounts.json</h3>
<code>
	{
	"fromAccount": {
		"client_id": "export account client id",
		"secret": "export account client secret"
	},
	
	"toAccount": {
		"client_id": "import account client id",
		"secret": "import account client secret"
	}
}
</code>

<h2>Usage</h2>
<ol> 
	<li>Open terminal/command prompt and navigate to the code directory.</li>
	<li>Create a new file in the same directory named 'accounts.json'.</li>
	<li>Copy and paste the code above into accounts.json, filling in your client ID and secret from Reddit.</li>
	<li>Enter `python main.py`</li>
	<li>Press Enter</li>
	<li>In your primary browser, sign in to the Reddit account you want to copy subscriptions from.</li>
	<li>Press Enter</li>
	<li>Be sure the click 'Accept' on the page that opens.</li>
	<li>In the same browser, log out of the current account and log into the Reddit account which you want to import subscriptions to.</li>
	<li>Press Enter</li>
	<li>Be sure the click 'Accept' on the page that opens.</li>
	<li>Press Enter. <b>Note: This will overwrite all subscriptions on the currently logged in account!</b></li>
	<li>Done</li>
</ol>

