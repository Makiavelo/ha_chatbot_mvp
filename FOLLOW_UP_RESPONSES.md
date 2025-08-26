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

**Monitoring:**
- **CloudWatch Metrics**: Track Lambda invocations, duration, errors, cold starts
- **X-Ray**: Trace request flow and identify bottlenecks
- **Custom metrics**: LLM response time, token usage, API call success rates
- **CloudWatch Logs Insights**: Query conversation logs for patterns

**Evaluation:**
- **Business Metrics**: 
  - Lead conversion rate (new pharmacy → scheduled callback)
  - Successful pharmacy identification rate
  - Average conversation duration
- **Quality Metrics**:
  - LLM response relevance (sample and review)
  - Conversation completion rate
  - User satisfaction (follow-up surveys)
  - Fallback/error rate
- **Alerts**: Set up SNS notifications for error rates, response times, budget thresholds