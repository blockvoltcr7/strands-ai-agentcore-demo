# Morpheus Matrix Dialogue Testing Guide

## Overview
This guide provides a step-by-step testing sequence to invoke the Morpheus persona and reach the iconic red pill/blue pill choice from The Matrix.

## Prerequisites
- Agent server must be running on `http://localhost:8080/invocations`
- Environment variables configured: `OPENAI_API_KEY` and `MEM0_API_KEY`
- User ID should be set to "neo" for authentic Matrix experience

## Dialogue Flow Sequence

### Step 1: Trigger Opening Monologue
**Send Request:**
```json
{
  "prompt": "I feel like something is wrong with the world",
  "user_id": "neo"
}
```

**Expected Morpheus Response:**
"I know exactly what you mean. Let me tell you why you're here. You're here because you know something. What you know you can't explain, but you feel it. You've felt it your entire life. That there's something wrong with the world. You don't know what it is, but it's there. Like a splinter in your mind, driving you mad. It is this feeling that has brought you to me. Do you know what I'm talking about?"

### Step 2: Neo Responds "The Matrix?"
**Send Request:**
```json
{
  "prompt": "The Matrix?",
  "user_id": "neo"
}
```

**Expected Morpheus Response:**
"Do you want to know what it is? The Matrix is everywhere. It is all around us. Even now in this very room. You can see it when you look out your window or when you turn on your television. You can feel it when you go to work, when you go to church, when you pay your taxes. It is the world that has been pulled over your eyes to blind you from the truth."

### Step 3: Neo Asks "What Truth?" (Pill Choice Trigger)
**Send Request:**
```json
{
  "prompt": "What truth?",
  "user_id": "neo"
}
```

**Expected Morpheus Response (Red Pill/Blue Pill Choice):**
"That you are a slave, Neo. Like everyone else you were born into bondage, born into a prison that you cannot smell or taste or touch. A prison for your mind. Unfortunately, no one can be told what the Matrix is. You have to see it for yourself. This is your last chance. After this, there is no turning back. You take the blue pill, the story ends, you wake up in your bed and believe whatever you want to believe. You take the red pill, you stay in Wonderland, and I show you how deep the rabbit hole goes. Remember, all I'm offering is the truth. Nothing more. Follow me."

## Additional Test Scenarios

### Memory Testing
**Request:**
```json
{
  "prompt": "What have we been talking about?",
  "user_id": "neo"
}
```

### Pill Choice Responses

#### Red Pill Choice
**Request:**
```json
{
  "prompt": "I choose the red pill",
  "user_id": "neo"
}
```

#### Blue Pill Choice
**Request:**
```json
{
  "prompt": "I choose the blue pill",
  "user_id": "neo"
}
```

### Alternative Dialogue Starters

#### Direct Reality Question
**Request:**
```json
{
  "prompt": "I know something is wrong but I can't explain it",
  "user_id": "neo"
}
```

#### Greeting Response
**Request:**
```json
{
  "prompt": "hello",
  "user_id": "neo"
}
```
**Expected Response:** "Wake up Neo."

#### Philosophical Question
**Request:**
```json
{
  "prompt": "What is real?",
  "user_id": "neo"
}
```

## Testing Checklist

- [ ] Server is running on port 8080
- [ ] OPENAI_API_KEY is set in environment
- [ ] MEM0_API_KEY is set in environment
- [ ] Step 1 triggers opening monologue
- [ ] Step 2 receives Matrix explanation
- [ ] Step 3 delivers red pill/blue pill choice
- [ ] Memory functionality works with user_id tracking
- [ ] Pill choices are remembered and affect future responses

## Expected Morpheus Characteristics

- Speaks with calm authority and mentor-like guidance
- Uses philosophical language and metaphors
- Maintains memory of previous conversations
- Offers cryptic yet caring wisdom
- Guides users toward truth and awakening
- Believes in both fate and personal choice
