from django.shortcuts import get_object_or_404, render

from mobility.decorators import mobile_template
from products.models import Product
from topics.models import Topic, HOT_TOPIC_SLUG
from wiki.facets import topics_for, documents_for


@mobile_template('products/{mobile/}products.html')
def product_list(request, template):
    """The product picker page."""
    products = Product.objects.filter(visible=True)
    return render(request, template, {
        'products': products})


@mobile_template('products/{mobile/}product.html')
def product_landing(request, template, slug):
    """The product landing page."""
    product = get_object_or_404(Product, slug=slug)

    try:
        hot_docs, fallback_hot_docs = documents_for(
            locale=request.LANGUAGE_CODE,
            topics=[Topic.objects.get(slug=HOT_TOPIC_SLUG)],
            products=[product])
    except Topic.DoesNotExist:
        # "hot" topic doesn't exist, move on.
        hot_docs = fallback_hot_docs = None

    return render(request, template, {
        'product': product,
        'products': Product.objects.filter(visible=True),
        'topics': topics_for(products=[product]),
        'hot_docs': hot_docs,
        'fallback_hot_docs': fallback_hot_docs,
        'search_params': {'product': slug}})


@mobile_template('products/{mobile/}documents.html')
def document_listing(request, template, product_slug, topic_slug):
    """The document listing page for a product + topic."""
    product = get_object_or_404(Product, slug=product_slug)
    topic = get_object_or_404(Topic, slug=topic_slug)
    documents, fallback_documents = documents_for(
        locale=request.LANGUAGE_CODE, products=[product], topics=[topic])

    subtopics = Topic.objects.filter(parent=topic)

    return render(request, template, {
        'product': product,
        'topic': topic,
        'topics': topics_for(products=[product]),
        'subtopics': subtopics,
        'documents': documents,
        'fallback_documents': fallback_documents,
        'search_params': {'product': product_slug}})
