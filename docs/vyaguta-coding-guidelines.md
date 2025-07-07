# Vyaguta Coding Guidelines and Best Practices

## 1. Extensions

Here are the list of extensions that you can use to make the development easier and save time:

- **Sonarlint** (https://www.sonarsource.com/products/sonarlint/) - Detect bugs, code smells, vulnerabilities plus security hotspots and many more
- **Mintlify** (https://writer.mintlify.com/) - Generate codebase documentation
- **Live Share** (https://code.visualstudio.com/learn/collaboration/live-share) - Easy collaboration during WFH
- **Prettier** (https://prettier.io/) - Code formatter to ensure consistent code style
- **ESLint** (https://eslint.org/) - Linter tool to find and fix problems in your JavaScript code

## 2. Import Orders

### Client Side Application

The codebase follows a ladder import pattern, grouping imports in a specific order:

1. Package third-party libraries
2. Icons
3. Assets icons
4. Components
5. Constants
6. Configuration
7. Slices
8. Interfaces
9. Utils
10. Hooks
11. Services
12. Other files

_Tip: Use the Bharyang extension in VS Code for auto-organizing imports._

### Server Side Application

Suggested import order:

1. Third-party libraries
2. Model
3. Common
4. Utils
5. Services
6. DTO
7. Validations
8. Other files

_Leave a line after each group of imports._

### Embracing Absolute Imports

Utilize absolute imports for clarity and maintainability. Adhere to established guidelines and practices within each module.

### Leaving a Line

Give space before declaring the return, before and after if/else statements, and after variable declarations.

```js
/**
 * Adds two numbers together.
 *
 * @returns {number} The sum of the two numbers.
 */
const add = () => {
  const a = 1;
  const b = 2;
  if (!a || !b) {
    return;
  }
  return a + b;
};
```

### Avoiding Console in the Codebase

Remove `console.log` statements before committing or deploying code. Use logging libraries for sophisticated logging.

### Utilizing Optional Chaining

Use optional chaining to safely access properties and methods:

```js
// Without optional chaining
const name = user && user.profile && user.profile.name;
// With optional chaining
const name = user?.profile?.name;
```

Combine with nullish coalescing operator for default values:

```js
const username = user?.profile?.username ?? "Guest";
```

### Using Ternary Operator

Use ternary for simple conditions, avoid nested ternaries for complex logic.

```js
const message = isLoggedIn ? "Welcome, user!" : "Please log in.";
```

### Avoiding Callback Hell

Use Promises or async/await for asynchronous operations. Modularize code and use helper functions. Use control flow libraries like `Promise.all`.

### Variable Names

- Use concise, descriptive names (3-10 characters)
- Avoid Hungarian notation
- Use plural for collections
- Use camelCase for primitives
- Avoid articles and possessives

### Variable Declarations

- Use `const` for variables that won't be reassigned
- Use `let` for variables that will be reassigned
- Avoid `var`
- Declare one variable per line

### Avoiding Deprecated APIs

- Use modern alternatives (e.g., `fetch` instead of XHR)
- Avoid deprecated interfaces (e.g., use `AudioWorklet` instead of `ScriptProcessorNode`)

### Avoid Mutations

- Use `const` for immutable values
- Avoid reassigning variables
- Use immutable data structures
- Prefer functional programming
- Avoid side effects

### JS Docs

- Document all public functions and classes with JSDoc
- Use `@param`, `@returns`, and `@throws` tags
- Keep comments up-to-date

```js
/**
 * Calculates the sum of two numbers.
 * @param {number} a - The first number.
 * @param {number} b - The second number.
 * @returns {number} The sum of the two numbers.
 */
function sum(a, b) {
  return a + b;
}
```

---

# What is a Pull Request (PR)?

A Pull Request (PR) is a request to merge your code changes from a feature branch into another branch (such as dev, QA, UAT, or main) in the repository. PRs allow team members to review, discuss, and approve changes before they are merged. This process helps maintain code quality and enables collaborative development.

# What are the environments: dev, QA, UAT, main/master/production?

In Vyaguta and most modern software projects, code is promoted through several environments before reaching end users. Each environment serves a specific purpose in the development and release process:

## dev (Development)

- **Purpose:** Where active development happens. Developers push and test new features, bug fixes, and experiments.
- **Who uses it:** Developers.
- **Why:** To integrate and test code changes early and often, catch issues quickly, and collaborate on new work.

## QA (Quality Assurance)

- **Purpose:** A stable environment for testers to verify new features, bug fixes, and overall system quality.
- **Who uses it:** QA engineers, testers, sometimes developers.
- **Why:** To ensure that new code works as expected and does not break existing functionality before it moves closer to production.

## UAT (User Acceptance Testing)

- **Purpose:** A pre-production environment where business stakeholders or end users validate that the system meets requirements.
- **Who uses it:** Product owners, business analysts, client representatives, sometimes QA.
- **Why:** To confirm that the software is ready for release and meets business needs. Only after UAT approval does code move to production.

## main/master/production

- **Purpose:** The live environment used by real users. Sometimes called `main`, `master`, or `production`.
- **Who uses it:** End users, customers, clients.
- **Why:** This is the final, stable version of the software. Only thoroughly tested and approved code is merged here. Direct pushes are strictly prohibited to maintain stability and reliability.

**Summary Table:**

| Environment | Who Uses It             | Purpose/Why                             |
| ----------- | ----------------------- | --------------------------------------- |
| dev         | Developers              | Active development and integration      |
| QA          | QA/Testers, Developers  | Testing and quality assurance           |
| UAT         | Product Owners, Clients | Business/user validation before release |
| main/master | End Users, Clients      | Live, stable, production-ready software |

**Best Practice:**

- Code should flow from dev → QA → UAT → main/master, with reviews and approvals at each stage. This ensures high quality and minimizes risk in production.

# Contributing

Our code repository is hosted on GitHub. If you don't have access yet, please reach out to your Project Manager (PM) or Team Lead (TL) for permissions.

## For PR Author

- **No direct pushes** to dev, QA, UAT, and main/master branches.
- PRs should not include excessive changes, except when merging into QA, UAT, and main/master.
- Create a branch named after the Jira ticket (e.g., `VGU-1023`). For bug fixes, use `VGU-1023-fix`.
- Checkout the branch: `git checkout -b VGU-1023`
- Implement changes as per Jira ticket and coding guidelines.
- Commit: `git commit -m "VGU-1023: Add new feature implementation"`
- Rebase if needed, then push: `git push origin VGU-1023`
- Create a pull request (PR) on GitHub. Use the PR template, mention Jira ticket, and assign yourself.
- Link the Jira ticket in the PR description.
- Assign reviewers.
- Update `.env.example` and README if needed.
- Submit the PR and share in the `vyaguta-github` Slack channel: `VGU-1023: Add new feature implementation.`
- Monitor and address feedback (icon 📝 means feedback required).
- After addressing feedback, commit changes (avoid `--amend` unless necessary), rebase, and notify team.
- Sync with base branch using rebase: `git pull origin <base_branch> -r`
- Merge after approval and checks. Merging team member will drop ✅ in Slack.

## For Reviewers

- Understand the context (read PR description and Jira ticket)
- Review code quality, naming, modularity, and comments
- Test changes locally
- Evaluate functionality against requirements
- Give clear, specific, and respectful feedback
- Consider maintainability (DRY, YAGNI, KISS, SOLID)
- Address security considerations
- Verify documentation updates
- Engage in discussions
- Be timely and respectful

---

# Logging Practices

Logging in a web application can be divided into three major components:

1. Request level logs
2. Application level logs (info, error, debug)
3. Exception logs

## 1. Application Level Logs

- Log format: `<timestamp> <log_level> <request_identifier> <file/namespace>: <Log Message>`
- Log at the top of each service layer
- Add logs between major tasks
- Log data length when processing chunks
- Log access restrictions with reasons
- Log resource id and user id for create/update/delete
- Mask critical data in logs
- Log errors in catch blocks
- Handle errors outside try/catch in middleware
- End logs with a full stop

## 2. Exception Logs

- Log uncaught exceptions and send to services like Sentry
- Example:

```js
process.on("uncaughtException", (err) => {
  logger.error("Uncaught exception", err);
  try {
    Sentry.captureException(err);
  } catch (err) {
    logger.error("Raven error", err);
  } finally {
    process.exit(1);
  }
});
```

## 3. Request Level Logging

- Log timestamp, method, URL, status code, client IP, agent, CPU time, content length, and unique request id
- Use logs to trace requests, find average CPU time, and record status codes

---

# Dependencies

- **vyaugta-icons**: Collection of icons for Vyaguta
- **Axios**: HTTP client for API requests
- **node-sass**: Styling with BEM methodology
- **express, NestJS**: Backend frameworks
- **webpack, vite**: Frontend bundlers
- **Redux**: State management (slice pattern)
- **Knex**: SQL query builder (no ORM)
- **@maskeynihal/mailer**: Email functionalities
- **@maskeynihal/pursue**: Vyaguta-specific module

Refer to individual `package.json` files for more details.

---

# Codebase Documentation

## Folder Structure

- **App folder**: Frontend code (components, containers, pages, utils, styles, etc.)
- **Server folder**: Backend code (controllers, models, routes, middleware, templates, database)
- **Root directory**: `package.json`, `eslint`, `pull_request_templated.md` for configs and hooks

This structure ensures clear separation between frontend and backend code.

# Vyaguta QA Onboarding Checklist

- [QA Onboarding Checklist (Google Sheet)](https://docs.google.com/spreadsheets/d/1-eJVhorK-LNWX9uZEv9FV9sGwc3NOlhLjLiu_r5XFpE/edit?gid=711236100#gid=711236100)

# Project Manager Onboarding

Welcome to the onboarding checklist page for newly appointed Project Managers joining our project Vyaguta. This comprehensive guide provides a step-by-step roadmap to ensure a smooth transition and a quick grasp of key responsibilities.

- [Project Manager Onboarding Checklist (Google Sheet)](https://docs.google.com/spreadsheets/d/1Ba-7RUlPWC1ba7-s92NC_g-VVYE-QFX72aFz7gUtxwA/edit?usp=sharing)
