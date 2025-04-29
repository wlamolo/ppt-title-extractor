# Narrative Feedback Feature Implementation Plan

## Overview
Add functionality to collect target audience information and provide AI-powered feedback on presentation narrative structure using OpenAI's API.

## Features
1. Target Audience Input Field
2. AI Feedback Generation
3. Feedback Display

## New Display Improvements

### Text Display Enhancement
- [ ] Replace "Page" with "p." in slide numbering
- [ ] Remove markdown-style bolding ("**")
- [ ] Improve overall text formatting for better readability

### Section Title Handling
- [ ] Identify section title slides (slides without headlines)
- [ ] Extract section titles from these slides if available
- [ ] Update the display logic to show section information appropriately
- [ ] Handle empty slides gracefully

## Technical Requirements

### Frontend Changes
- [ ] Add target audience input field to the main form
- [ ] Add "Get Feedback" button component
- [ ] Create feedback display component
- [ ] Add loading state for API calls
- [ ] Style new components to match existing design

### Backend Changes
- [ ] Add OpenAI API integration
- [ ] Create new endpoint for feedback generation
- [ ] Update text file processing to include audience information
- [ ] Implement error handling for API calls
- [ ] Modify `extract_titles` endpoint to:
  - Extract section titles from slides
  - Identify section introduction slides
  - Include section information in the response structure
- [ ] Update PowerPoint processing logic to handle different slide types
- [ ] Create a more structured response format that includes both titles and section information

### API Integration
- [ ] Add OpenAI API key configuration
- [ ] Implement prompt template with audience insertion
- [ ] Handle API rate limiting and errors

## Implementation Checklist

### Phase 1: Frontend Setup
1. [ ] Add target audience input field to form component
2. [ ] Add state management for audience field
3. [ ] Create feedback button component
4. [ ] Create feedback display component
5. [ ] Add loading states and error handling UI

### Phase 2: Backend Integration
1. [ ] Set up OpenAI API client
2. [ ] Create feedback generation endpoint
3. [ ] Implement prompt template
4. [ ] Add error handling middleware

### Phase 3: Testing & Polish
1. [ ] Test audience input validation
2. [ ] Test API integration
3. [ ] Test error scenarios
4. [ ] Add loading indicators
5. [ ] Style polish and UI improvements

## API Endpoint Design

```
POST /api/generate-feedback
Request Body:
{
    "presentationText": string,
    "targetAudience": string
}

Response:
{
    "feedback": {
        "introduction": string,
        "transitions": string,
        "organization": string
    }
}
```

## Dependencies to Add
- OpenAI Node package (backend)
- Any additional UI components needed

## Security Considerations
- Secure storage of OpenAI API key
- Rate limiting for API calls
- Input validation
- Error handling

## Testing Strategy
- Unit tests for new components
- Integration tests for API endpoints
- End-to-end testing of feedback flow

## Commit Strategy
1. Frontend form updates
2. Backend API setup
3. Integration implementation
4. UI polish and error handling
5. Testing and documentation 

## Implementation Steps

1. Backend Updates
   - [ ] Analyze PowerPoint slide layouts to identify section slides
   - [ ] Extract section information from slides
   - [ ] Modify the response structure to include section data
   - [ ] Update text formatting for slide numbers

2. Frontend Updates
   - [ ] Update the title display component
   - [ ] Add styling for section titles
   - [ ] Implement new formatting for slide numbers
   - [ ] Add visual hierarchy between sections and slides

3. Testing
   - [ ] Test with various PowerPoint layouts
   - [ ] Verify section title extraction
   - [ ] Check formatting consistency
   - [ ] Test with empty slides and edge cases

## Original Features (Completed)
1. Target Audience Input Field
2. AI Feedback Generation
3. Feedback Display 