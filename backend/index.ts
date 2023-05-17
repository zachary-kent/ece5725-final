import express from 'express'
import { verify } from 'jsonwebtoken';
import { IncorrectPassword, UserNotFound, createUser, highScore, highScores, login, setHighScore } from './user';
import { serve, setup } from 'swagger-ui-express'
import docs from './docs.json'

/** The express application */
const app = express();

// Parse request bodies as JSON
app.use(express.json())

// Setup the documentation endpoint
app.use('/docs', serve, setup(docs))


/**
 * Middleware for authenticating an access token and saving it in the
 * locals of a request.
 * 
 * @param req The HTTP request
 * @param res The HTTP response
 * @param next The next middleware in the application cycle
 * @returns the reponse
 */
const validateToken = async (req, res, next) => {
  const token = req.headers['x-access-token'];
  if (token == null) {
    return res.status(401).send("Access token required");
  }
  try {
    // Get username token was signed with
    const username = verify(token, process.env.SECRET);
    // Save username in locals of request
    res.locals.username = username;
  } catch {
    // Token malformed
    return res.status(403).send("Invalid access token");
  }
  return next();
}

// Endpoint for creating an account
app.post('/register', async (req, res) => {
  const { username, password } = req.body;
  if (username == null || password == null) {
    // Malformed request body
    return res.status(400).send("Username and password required");
  }
  try {
    // Create user in database
    await createUser({ username, password });
    return res.status(200).send("User created");
  } catch {
    // Duplicate user
    return res.status(400).send("User already exists");
  }
});

// Endpoint for logging in an obtaining access token
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  if (username == null || password == null) {
    // Malformed request body
    return res.status(400).send('Username and password required');
  }
  try {
    // Get access token from logging in
    const token = await login({ username, password });
    // Send it back to user
    return res.status(200).send({ token });
  } catch (e) {
    if (e instanceof IncorrectPassword) {
      // User provided incorrect password
      return res.status(400).send('Incorrect password');
    }
    if (e instanceof UserNotFound) {
      // User does not exist
      return res.status(400).send('User not found');
    }
    return res.status(400).send('Invalid credentials');
  }
})

// Endpoint for updating a user's high score
app.post('/high-score', validateToken, async (req, res) => {
  const { score } = req.body;
  if (score == null) {
    // Malformed request body
    return res.status(400).send("Score required");
  }
  try {
    // Set high score in database
    await setHighScore(res.locals.username, score);
    return res.status(200).send("High score updated");
  } catch {
    // Only occurs when user not found in database
    return res.status(400).send("User not found");
  }
});

// Endpoint for retrieving a user's high score
app.get('/high-score', validateToken, async (req, res) => {
  try {
    // Get score of user associated with access token
    const score = await highScore(res.locals.username);
    return res.status(200).send({ score })
  } catch {
    // User not found
    return res.status(400).send("User not found");
  }
});

app.get('/high-score/rankings', async (req, res) => {
  try {
    const { limit } = req.query;
    if (limit == null) {
      // Send back all high scores
      const scores = await highScores();
      return res.status(200).send({ scores })
    }
    if (typeof limit !== 'string') {
      // limit has incorrect type
      return res.status(400).send('Limit has incorrect type');
    }
    // Parse string given representing limit
    const max = parseInt(limit, 10);
    if (Number.isNaN(max)) {
      // limit string does not represent number
      return res.status(400).send('Cannot parse limit');
    }
    const scores = await highScores(max);
    return res.status(200).send({ scores })
  } catch {
    return res.sendStatus(400);
  }
});

/** The port the app will accept requests from */
const port = process.env.PORT || 8080;

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
})
