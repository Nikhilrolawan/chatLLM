from fastapi import APIRouter, Depends, HTTPException
from models import model
from db.engine import get_db
from middlewares import user as usermw
from schemas import schema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat(
    body: schema.ChatMessage,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(usermw.get_current_user),
):
    if body.conversation_id:
        query = select(model.Conversation).where(
            model.Conversation.id == body.conversation_id
        )
        res = await db.execute(query)
        conversation = res.scalar_one_or_none()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        if conversation.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not your Conversation")
    else:
        conversation = model.Conversation(
            user_id=current_user.user_id, title=body.content[:50]
        )
        db.add(conversation)
        await db.flush()

    message = model.Message(
        conversation=conversation.id, content=body.content, role="user"
    )
    db.add(message)
    await db.flush()
    query = (
        select(model.Message)
        .where(model.Message.conversation_id == conversation.id)
        .order_by(model.Message.created_at)
    )
    res = await db.execute(query)
    history = res.scalars().all()
    llm_response = await llm.get_response(history)

    db.add(
        model.Message(
            conversation = conversation.id, content = llm_response, role = "assistant"
        )
    )
    await db.commit()

    return {
        "conversation_id": conversation.id,
        "response": llm_response
    }
