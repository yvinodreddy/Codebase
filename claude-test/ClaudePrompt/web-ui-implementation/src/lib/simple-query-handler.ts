/**
 * Simple Query Handler
 *
 * Detects simple queries (math, definitions, etc.) and provides direct answers
 * without ULTRATHINK framework overhead. For complex queries, uses full ULTRATHINK.
 */

export interface SimpleQueryResult {
  isSimple: boolean;
  answer?: string;
  confidence?: number;
}

/**
 * Detect if query is simple enough for direct answer
 */
export function detectSimpleQuery(query: string): SimpleQueryResult {
  const normalized = query.toLowerCase().trim();

  // Math expressions
  const mathPattern = /^(what is |calculate |compute |solve )?[\d\s\+\-\*\/\(\)\^\.]+(\?)?$/i;
  if (mathPattern.test(normalized)) {
    return handleMathQuery(query);
  }

  // Simple factual questions
  const simpleFactPatterns = [
    /^what is (\d+) ?\+ ?(\d+)\??$/i,  // "what is 2+2?"
    /^(\d+) ?\+ ?(\d+) ?= ?\??$/i,     // "2+2=?"
    /^calculate (\d+) ?\+ ?(\d+)\??$/i, // "calculate 2+2"
  ];

  for (const pattern of simpleFactPatterns) {
    const match = normalized.match(pattern);
    if (match) {
      return handleMathQuery(query);
    }
  }

  // Not a simple query - needs ULTRATHINK
  return { isSimple: false };
}

/**
 * Handle mathematical queries
 */
function handleMathQuery(query: string): SimpleQueryResult {
  try {
    // Extract the mathematical expression
    const normalized = query.toLowerCase().trim();
    let expression = normalized;

    // Remove common prefixes
    expression = expression.replace(/^(what is|calculate|compute|solve)\s+/i, '');
    expression = expression.replace(/\?+$/g, ''); // Remove trailing ?
    expression = expression.trim();

    // Simple addition pattern
    const addMatch = expression.match(/^(\d+)\s*\+\s*(\d+)$/);
    if (addMatch) {
      const num1 = parseInt(addMatch[1]);
      const num2 = parseInt(addMatch[2]);
      const result = num1 + num2;

      return {
        isSimple: true,
        answer: formatMathAnswer(num1, num2, result, '+'),
        confidence: 100.0
      };
    }

    // Simple subtraction
    const subMatch = expression.match(/^(\d+)\s*-\s*(\d+)$/);
    if (subMatch) {
      const num1 = parseInt(subMatch[1]);
      const num2 = parseInt(subMatch[2]);
      const result = num1 - num2;

      return {
        isSimple: true,
        answer: formatMathAnswer(num1, num2, result, '-'),
        confidence: 100.0
      };
    }

    // Simple multiplication
    const mulMatch = expression.match(/^(\d+)\s*[\*x×]\s*(\d+)$/i);
    if (mulMatch) {
      const num1 = parseInt(mulMatch[1]);
      const num2 = parseInt(mulMatch[2]);
      const result = num1 * num2;

      return {
        isSimple: true,
        answer: formatMathAnswer(num1, num2, result, '×'),
        confidence: 100.0
      };
    }

    // Simple division
    const divMatch = expression.match(/^(\d+)\s*[\/÷]\s*(\d+)$/);
    if (divMatch) {
      const num1 = parseInt(divMatch[1]);
      const num2 = parseInt(divMatch[2]);
      if (num2 === 0) {
        return {
          isSimple: true,
          answer: `## Mathematical Error\n\n**Division by zero is undefined.**\n\n${num1} ÷ 0 = undefined\n\nDivision by zero is not permitted in mathematics.`,
          confidence: 100.0
        };
      }
      const result = num1 / num2;
      const resultStr = Number.isInteger(result) ? result.toString() : result.toFixed(2);

      return {
        isSimple: true,
        answer: `## Answer\n\n**${num1} ÷ ${num2} = ${resultStr}**\n\n### Explanation\n\nWhen you divide ${num1} by ${num2}, you get ${resultStr}.\n\n*Confidence: 100%*`,
        confidence: 100.0
      };
    }

    // Not a simple math expression
    return { isSimple: false };

  } catch (error) {
    // If parsing fails, treat as complex query
    return { isSimple: false };
  }
}

/**
 * Format math answer with explanation
 */
function formatMathAnswer(num1: number, num2: number, result: number, operator: string): string {
  const operatorNames: Record<string, string> = {
    '+': 'addition',
    '-': 'subtraction',
    '×': 'multiplication',
    '÷': 'division'
  };

  return `## Answer

**${num1} ${operator} ${num2} = ${result}**

### Explanation

This is a simple ${operatorNames[operator]} operation:
- First number: ${num1}
- Second number: ${num2}
- Result: **${result}**

### Mathematical Context

${getMathContext(operator, num1, num2, result)}

*Confidence: 100%*
`;
}

/**
 * Get mathematical context based on operation
 */
function getMathContext(operator: string, num1: number, num2: number, result: number): string {
  switch (operator) {
    case '+':
      return `Addition combines two numbers into a sum. When you add ${num1} and ${num2}, you're combining them to get ${result}. This follows the commutative property: ${num1} + ${num2} = ${num2} + ${num1}.`;

    case '-':
      return `Subtraction finds the difference between two numbers. When you subtract ${num2} from ${num1}, you get ${result}. Unlike addition, subtraction is not commutative: ${num1} - ${num2} ≠ ${num2} - ${num1}.`;

    case '×':
      return `Multiplication is repeated addition. ${num1} × ${num2} means adding ${num1} to itself ${num2} times, which equals ${result}. This follows the commutative property: ${num1} × ${num2} = ${num2} × ${num1}.`;

    case '÷':
      return `Division splits a number into equal parts. ${num1} ÷ ${num2} means dividing ${num1} into ${num2} equal parts, giving ${result} per part.`;

    default:
      return '';
  }
}
