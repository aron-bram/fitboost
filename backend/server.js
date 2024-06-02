import express from 'express';
import { Sequelize } from 'sequelize';
import cors from 'cors';

const app = express();
const port = 5000;

app.use(cors());
app.use(express.json());

// Initialize Sequelize
const sequelize = new Sequelize({
    dialect: 'postgres',
    database: 'fitboost',
    user: 'baron',
    host: '/var/run/postgresql',
    port: 5432,
    ssl: true,
    clientMinMessages: 'notice',
});

// Test the database connection
sequelize.authenticate()
  .then(() => console.log('Database connected'))
  .catch(err => console.error('Unable to connect to the database:', err));

app.get('/', (_req, res) => {
  res.send('Hello World!');
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});