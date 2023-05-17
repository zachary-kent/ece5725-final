import express from 'express'
import { verify } from 'jsonwebtoken';
import { IncorrectPassword, UserNotFound, createUser, highScore, highScores, login, setHighScore } from './user';
import { serve, setup } from 'swagger-ui-express'
import docs from './docs.json'

const app = express();

app.use(express.json())

app.use('/docs', serve, setup(docs))

const validateToken = async (req, res, next) => {
  const token = req.headers['x-access-token'];
  if (token == null) {
    return res.status(401).send("Access token required");
  }
  try {
    const username = verify(token, process.env.SECRET);
    res.locals.username = username;
  } catch {
    return res.status(403).send("Invalid access token");
  }
  return next();
}

app.post('/register', async (req, res) => {
  const { username, password } = req.body;
  if (username == null || password == null) {
    return res.status(400).send("Username and password required");
  }
  try {
    await createUser({ username, password });
    return res.status(200).send("User created");
  } catch {
    return res.status(400).send("User already exists");
  }
});

app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  if (username == null || password == null) {
    return res.status(400).send('Username and password required');
  }
  try {
    const token = await login({ username, password });
    return res.status(200).send({ token });
  } catch (e) {
    if (e instanceof IncorrectPassword) {
      return res.status(400).send('Incorrect password');
    }
    if (e instanceof UserNotFound) {
      return res.status(400).send('User not found');
    }
    return res.status(400).send('Invalid credentials');
  }
})

app.post('/high-score', validateToken, async (req, res) => {
  const { score } = req.body;
  if (score == null) {
    return res.status(400).send("Score required");
  }
  try {
    await setHighScore(res.locals.username, score);
    return res.status(200).send("High score updated");
  } catch {
    return res.status(400).send("User not found");
  }
});

app.get('/high-score', validateToken, async (req, res) => {
  try {
    const score = await highScore(res.locals.username);
    return res.status(200).send({ score })
  } catch {
    return res.status(400).send("User not found");
  }
});

app.get('/high-score/rankings', async (req, res) => {
  try {
    const { limit } = req.query;
    if (limit == null) {
      const scores = await highScores();
      return res.status(200).send({ scores })
    }
    if (typeof limit !== 'string') {
      return res.status(400).send('Limit has incorrect type');
    }
    const max = parseInt(limit, 10);
    if (Number.isNaN(max)) {
      return res.status(400).send('Cannot parse limit');
    }
    const scores = await highScores(max);
    return res.status(200).send({ scores })
  } catch {
    return res.sendStatus(400);
  }
});

const port = process.env.PORT || 8080;

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
})
