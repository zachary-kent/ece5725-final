import express from 'express'
import { verify } from 'jsonwebtoken';
import { IncorrectPassword, UserNotFound, createUser, highScore, highScores, login, setHighScore } from './user';

const app = express();

app.use(express.json())

const validateToken = async (req, res, next) => {
  const token = req.headers['x-access-token'];
  if (token == null) {
    return res.sendStatus(401);
  }
  try {
    const username = verify(token, process.env.SECRET);
    res.locals.username = username;
  } catch {
    return res.sendStatus(403);
  }
  return next();
}

app.post('/register', async (req, res) => {
  const { username, password } = req.body;
  if (username == null || password == null) {
    return res.sendStatus(400);
  }
  try {
    await createUser({ username, password });
    return res.sendStatus(200);
  } catch {
    return res.sendStatus(400);
  }
});

app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  if (username == null || password == null) {
    return res.status(400).send('Username and password must be provided');
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
    return res.sendStatus(400);
  }
  try {
    await setHighScore(res.locals.username, score);
    return res.sendStatus(200);
  } catch {
    return res.sendStatus(400);
  }
});

app.get('/high-score', validateToken, async (req, res) => {
  try {
    const score = await highScore(res.locals.username);
    return res.status(200).send({ score })
  } catch {
    return res.sendStatus(400);
  }
});

app.get('/high-score/rankings', async (req, res) => {
  const { limit } = req.body;
  try {
    const scores = highScores(limit);
    return res.status(200).send({ scores })
  } catch {
    return res.sendStatus(400);
  }
});

const port = process.env.PORT || 8080;

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
})
