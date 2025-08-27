# Follow-up Questions - Responses

## 1. How would you deploy this LLM response generation component over AWS?

I would deploy using **AWS Lambda** with API Gateway as the entry point. 

### Architecture Components:
- **API Gateway** → **Lambda Function** → **OpenAI API**
- **DynamoDB** for key-value stores only (session IDs, temporary state) - fast access
- **MongoDB/PostgreSQL** for persistent data:
  - MongoDB: Flexible schema for conversation logs
  - PostgreSQL: Structured metrics and reporting
- **Secrets Manager** for API keys
- **CloudWatch** for logs and metrics
- **SQS** for async processing if response times exceed limits

### Why Lambda:
- Serverless auto-scaling matches sporadic pharmacy call patterns
- Pay-per-execution cost model
- 15-minute timeout sufficient for LLM interactions
- Native AWS service integration

**Important:** Keep Lambda warm with scheduled CloudWatch Events (every 5-10 mins) to prevent cold start timeouts during low traffic periods.

### Deployment Strategy:
**Infrastructure as Code:** **Pulumi** with Python
- Native Python support matches project language
- Type-safe infrastructure definitions
- Superior IDE support vs CloudFormation/CDK
- Simplified state management

**CI/CD Pipeline:** **GitHub Actions**
- Automated testing on PRs
- Staging deployment on main branch merge
- Manual production approval gates
- Integrated Pulumi actions for infrastructure updates

## 2. How would you monitor and evaluate its performance when it's in production?

**Infrastructure Monitoring:**
- **CloudWatch**: Lambda metrics (invocations, duration, errors, cold starts)
- **X-Ray**: Request tracing and bottleneck identification
- **CloudWatch Logs Insights**: Query patterns in conversation logs

**Performance Metrics:**
- **Business KPIs**: Lead conversion rate, pharmacy identification rate, avg conversation duration
- **System Performance**: API call success rate, response latency (P50/P95/P99), token usage/cost
- **Conversation Quality**: Completion rate, user satisfaction, fallback/error rate

**LLM-Specific Evals:**
- **Automated Testing**: Accuracy tests, hallucination detection, API data consistency checks
- **Conversation Analysis**: Intent recognition rate, context retention, prompt injection resistance
- **Human Review**: Sample scoring for quality, edge case collection
- **Tools**: LangSmith for experiment tracking, custom eval suite for automated testing

**Alerting**: SNS notifications for error thresholds, response times, budget limits, eval score degradation