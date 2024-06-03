import express from "express";
import { Sequelize, DataTypes } from "sequelize";
import cors from "cors";

const app = express();
const port = 5000;

app.use(cors());
app.use(express.json());

// Initialize Sequelize
const sequelize = new Sequelize({
  dialect: "postgres",
  database: "fitboost",
  user: "baron",
  host: "/var/run/postgresql",
  port: 5432,
  ssl: true,
  dialectOptions: "notice",
});

// Define the Employee model to reference an existing table
const Employee = sequelize.define(
  "Employee",
  {
    id: {
      primaryKey: true,
      autoIncrement: true,
      type: DataTypes.INTEGER,
    },
    name: {
      type: DataTypes.STRING,
    },
    position: {
      type: DataTypes.STRING,
    },
    salary: {
      type: DataTypes.INTEGER,
    },
  },
  {
    tableName: "employees",
    timestamps: false,
  },
);

// Test the database connection
sequelize
  .authenticate()
  .then(() => console.log("Database connected"))
  .catch((err) => console.error("Unable to connect to the database:", err));

app.get("/", (_req, res) => {
  res.send("Hello World!");
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});

// Query all employees
app.get("/employees", async (_req, res) => {
  try {
    const employees = await Employee.findAll({});
    res.json(employees);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Add a new employee
app.post("/employees", async (req, res) => {
  try {
    const { name, position, salary } = req.body;
    const newEmployee = await Employee.create({ name, position, salary });
    res.status(201).json(newEmployee);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// Delete an employee by id
app.delete("/employees/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const deleted = await Employee.destroy({ where: { id } });
    if (deleted) {
      res.status(204).send(); // No Content
    } else {
      res.status(404).json({ error: "Employee not found" });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
