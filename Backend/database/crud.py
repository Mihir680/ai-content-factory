from sqlalchemy.orm import Session

from Backend.database.models import Content


def save_content(
    db: Session,
    topic,
    language,
    platform,
    tone,
    length,
    script,
    seo,
    description,
    hashtags,
    thumbnail,
    titles,
):
    content = Content(
        topic=topic,
        language=language,
        platform=platform,
        tone=tone,
        length=length,
        script=script,
        seo=seo,
        description=description,
        hashtags=hashtags,
        thumbnail=thumbnail,
        titles=titles,
    )

    db.add(content)
    db.commit()
    db.refresh(content)

    return content