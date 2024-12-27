# Install Node.js:

```
# installs nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

# download and install Node.js (you may need to restart the terminal)
nvm install 22

# verifies the right Node.js version is in the environment
node -v # should print `v22.11.0`

# verifies the right npm version is in the environment
npm -v # should print `10.9.0`
```

# Install promotofoo:

```
npx promptfoo@latest

```

# Add to .env OPENAI_API_KEY

To run:

```
npx promptfoo@latest eval
```

Afterwards, you can view the results by running `npx promptfoo@latest view`
