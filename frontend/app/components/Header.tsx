import { Button } from "react-bootstrap";

// Generated by Discord Application under OAuth2 > URL Generator with Scopes: identity
const href =
  "https://discord.com/api/oauth2/authorize?client_id=1154647072138608694&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fdashboard&response_type=token&scope=guilds%20identify";

export default function Header() {
  return (
    <>
      <header>zoe, the aspect of twighlight</header>
      <Button href={href}>Login with Discord</Button>
    </>
  );
}
